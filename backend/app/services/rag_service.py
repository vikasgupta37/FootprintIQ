"""
RAG Service — handles document embeddings and semantic search in Pinecone.
Falls back to a local search index if Pinecone is not configured.
"""

from typing import List, Dict, Any, Optional
from pinecone import Pinecone
from app.core.config import settings
from app.core.logging import logger
import re

# Local Mock Knowledge Base for offline/dev fallback
LOCAL_KNOWLEDGE_BASE = [
    {
        "id": "kb_food_1",
        "title": "Carbon Footprint of Food Production",
        "content": "Food production accounts for about 26% of global greenhouse gas emissions. Meat and other animal products are the highest contributors. Producing 1kg of beef results in approximately 60kg of greenhouse gases, while 1kg of peas produces less than 1kg.",
        "category": "food",
        "source": "Oxford University Study, 2018",
        "tags": ["food", "diet", "agriculture", "beef"]
    },
    {
        "id": "kb_trans_1",
        "title": "Transportation Emissions Comparison",
        "content": "Average emissions per passenger-kilometer: domestic flight (255g CO2e), driving a medium petrol car (192g), electric vehicle (53g based on standard grid mix), bus (105g), rail/train (41g). Shifting from solo driving to public transit reduces transport emissions by up to 70%.",
        "category": "transportation",
        "source": "UK Department for Environment, Food & Rural Affairs (DEFRA)",
        "tags": ["transportation", "ev", "flights", "travel"]
    },
    {
        "id": "kb_energy_1",
        "title": "Home Energy Efficiency",
        "content": "Heating and cooling make up over 50% of an average home's energy use. Setting thermostats to 68°F (20°C) in winter and 78°F (26°C) in summer saves up to 10% in heating/cooling costs. Upgrading to LED bulbs reduces lighting energy consumption by 75-80%.",
        "category": "energy",
        "source": "US Department of Energy",
        "tags": ["energy", "home", "heating", "led"]
    },
    {
        "id": "kb_waste_1",
        "title": "Waste Management and Landfills",
        "content": "Food waste in landfills decays anaerobically, generating methane, a greenhouse gas 28-36 times more potent than carbon dioxide. Composting organic waste prevents methane production. Recycling aluminum saves 95% of the energy needed to make new aluminum from scratch.",
        "category": "waste",
        "source": "US Environmental Protection Agency (EPA)",
        "tags": ["waste", "recycling", "composting", "methane"]
    },
    {
        "id": "kb_general_1",
        "title": "Greenhouse Gas Scopes (1, 2, and 3)",
        "content": "Scope 1 emissions are direct emissions from owned or controlled sources (e.g. burning gas in a company vehicle). Scope 2 are indirect emissions from the generation of purchased energy (e.g. electricity). Scope 3 includes all other indirect emissions in a company's value chain (e.g. business travel, supply chain).",
        "category": "sustainability_science",
        "source": "GHG Protocol Standard",
        "tags": ["scope", "accounting", "corporate", "ghg"]
    },
    {
        "id": "kb_offset_1",
        "title": "Carbon Offsetting Best Practices",
        "content": "Carbon offsetting involves compensating for emissions by funding equivalent carbon dioxide savings elsewhere. Look for offset projects certified by Gold Standard, Verified Carbon Standard (VCS), or Climate Action Reserve to ensure they are additional, permanent, and verified.",
        "category": "offsetting",
        "source": "WWF Guide to Carbon Offsets",
        "tags": ["offsetting", "forestry", "renewable", "carbon"]
    }
]

class RAGService:
    def __init__(self):
        self.pinecone_ready = False
        self.pc: Optional[Pinecone] = None
        self.index = None

        if settings.PINECONE_API_KEY:
            try:
                self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
                self.index = self.pc.Index(settings.PINECONE_INDEX_NAME)
                self.pinecone_ready = True
                logger.info("Pinecone RAG Service initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Pinecone: {e}. Running with local fallback.")

    async def search(self, query: str, namespace: str = "general", limit: int = 3) -> List[Dict[str, Any]]:
        """
        Search for relevant documentation.
        Attempts vector search if Pinecone is configured, otherwise falls back to local keyword matching.
        """
        if self.pinecone_ready and self.pc and self.index:
            try:
                # Generate embedding using Pinecone's built-in inference
                embeddings_response = self.pc.inference.embed(
                    model="multilingual-e5-large",
                    inputs=[query],
                    parameters={"input_type": "query"}
                )
                query_vector = embeddings_response.data[0].values

                # Query Pinecone
                query_response = self.index.query(
                    namespace=namespace,
                    vector=query_vector,
                    top_k=limit,
                    include_metadata=True
                )

                results = []
                for match in query_response.matches:
                    results.append({
                        "id": match.id,
                        "score": match.score,
                        "title": match.metadata.get("title", "Untitled Document"),
                        "content": match.metadata.get("content", ""),
                        "category": match.metadata.get("category", namespace),
                        "source": match.metadata.get("source", "Pinecone Knowledge Base")
                    })
                return results
            except Exception as e:
                logger.error(f"Pinecone vector search error: {e}. Falling back to local index.")

        # Local Keyword Fallback
        return self._local_search(query, limit)

    def _local_search(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Simple keyword matching fallback for development."""
        words = re.findall(r'\w+', query.lower())
        scored_docs = []

        for doc in LOCAL_KNOWLEDGE_BASE:
            score = 0
            # Title matches have high weight
            for word in words:
                if word in doc["title"].lower():
                    score += 5
                if word in doc["content"].lower():
                    score += 1
                for tag in doc.get("tags", []):
                    if word in tag.lower():
                        score += 3
            
            if score > 0:
                scored_docs.append((score, doc))

        # Sort by score descending
        scored_docs.sort(key=lambda x: x[0], reverse=True)

        results = []
        for score, doc in scored_docs[:limit]:
            results.append({
                "id": doc["id"],
                "score": float(score),
                "title": doc["title"],
                "content": doc["content"],
                "category": doc["category"],
                "source": doc["source"]
            })

        # If no results matched, return the top default docs to give the AI *some* context
        if not results:
            for doc in LOCAL_KNOWLEDGE_BASE[:limit]:
                results.append({
                    "id": doc["id"],
                    "score": 0.0,
                    "title": doc["title"],
                    "content": doc["content"],
                    "category": doc["category"],
                    "source": doc["source"]
                })

        return results

    async def index_document(self, doc_id: str, text: str, metadata: dict, namespace: str = "general") -> bool:
        """Uploads a document vector to Pinecone."""
        if not (self.pinecone_ready and self.pc and self.index):
            logger.warning("Pinecone not ready. Cannot index document.")
            return False

        try:
            # Generate embedding
            embeddings_response = self.pc.inference.embed(
                model="multilingual-e5-large",
                inputs=[text],
                parameters={"input_type": "passage"}
            )
            vector = embeddings_response.data[0].values

            # Insert document
            metadata["content"] = text
            self.index.upsert(
                vectors=[{
                    "id": doc_id,
                    "values": vector,
                    "metadata": metadata
                }],
                namespace=namespace
            )
            return True
        except Exception as e:
            logger.error(f"Failed to index document in Pinecone: {e}")
            return False

rag_service = RAGService()
