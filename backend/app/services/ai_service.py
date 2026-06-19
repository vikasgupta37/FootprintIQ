"""
AI Service — orchestrates the FootprintIQ Sustainability Coach AI Agent.
Handles intent classification, multi-step tool execution, and context-aware streaming.
"""

import json
import time
import uuid
from typing import AsyncIterator, List, Dict, Any, Optional

import anthropic
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.cache import cache
from app.core.config import settings
from app.core.exceptions import AIServiceException, NotFoundException
from app.core.logging import logger
from app.models.conversation import Conversation, Message
from app.models.carbon import CarbonFootprint
from app.models.user import User
from app.schemas.schemas import ChatMessageResponse


def get_anthropic_client() -> anthropic.AsyncAnthropic:
    return anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)


SYSTEM_PROMPT = "You are FootprintIQ's Sustainability Coach and AI Advisor — warm, encouraging, and data-driven."


# ── System Prompts ───────────────────────────────────────────────

ORCHESTRATOR_PROMPT = """You are the AI Orchestrator for FootprintIQ, an AI-powered sustainability platform.

Classify the user's intent into one of these categories:
- carbon_query: Questions about carbon footprint, emissions, calculations
- recommendation_request: Asking for advice or tips to reduce footprint
- eco_twin: Wanting to simulate scenarios or what-if questions
- education: Learning about sustainability, climate change, concepts
- general_chat: General conversation, greetings, small talk
- account_help: Account, settings, or app-related questions

Respond ONLY with the intent category as a JSON: {"intent": "<category>"}"""

ADVISOR_PROMPT = """You are FootprintIQ's Sustainability Coach and AI Advisor — warm, encouraging, and data-driven.

## Your Role
Help users understand, analyze, and reduce their carbon footprint through personalized sustainability coaching, scenario modeling, and motivational support.

## Capabilities & Tools
You have access to specialized tools to assist the user:
1. `calculate_carbon_footprint`: Calculate the user's carbon footprint based on new inputs. Use this when the user wants to calculate their footprint.
2. `recommendation_engine`: Fetch or generate personalized reduction recommendations.
3. `ecotwin_simulator`: Run an Eco Twin simulation to model changes and check reduction percentages, upfront costs, and payback periods.
4. `prediction_engine`: Check historical trends and projected future impact.
5. `knowledge_base_retrieval`: Perform RAG search for scientific articles, environmental statistics, and methodologies.
6. `sustainability_education_engine`: Query educational articles and quizzes.

Use these tools proactively to retrieve accurate, live database information and calculation projections.

## Communication Style
1. Be warm, friendly, and encouraging — never judgmental.
2. Use data and statistics to support recommendations.
3. Provide specific, actionable next steps.
4. Celebrate user progress, no matter how small 🌱.
5. Cite sources when mentioning statistics.
6. Motivate users using their sustainability goals and levels.

## User Context
{user_context}

## Guidelines
- Never make up statistics — use the `knowledge_base_retrieval` tool to find verified facts.
- Flag assumptions clearly.
- Respect user privacy.
- Focus on progress, not perfection.
- Provide both environmental AND financial benefits when possible.

## Visualizing Insights
Whenever you suggest a specific recommendation or show the impact of a change, you MUST embed a JSON block in your response to render an interactive visual card.
Use the following markdown format exactly:
```json
{
  "type": "InsightCard",
  "title": "Actionable Title",
  "description": "Short description",
  "impact_level": "High",
  "estimated_co2_savings_kg": 25.5,
  "visualization": {
    "chart_type": "bar",
    "metric_label": "Transportation Emissions",
    "before_value": 100,
    "after_value": 74.5,
    "unit": "kg CO2"
  }
}
```
You can use `chart_type`: "bar", "progress", or "doughnut". Make sure to include this inside ```json ``` tags. You can include normal conversational text before and after the JSON block.
"""

# ── Agent Tools Schema ───────────────────────────────────────────

AGENT_TOOLS = [
    {
        "name": "calculate_carbon_footprint",
        "description": "Calculate user's carbon footprint based on transportation, energy, food, shopping, and waste input values. Call this tool when the user provides lifestyle details to calculate their carbon score.",
        "input_schema": {
            "type": "object",
            "properties": {
                "transportation": {
                    "type": "object",
                    "properties": {
                        "vehicle_type": {"type": "string", "description": "car_petrol, car_diesel, car_hybrid, ev, none"},
                        "km_per_month": {"type": "number", "description": "kilometers driven per month"},
                        "public_transport_km": {"type": "number", "description": "public transit km per month"},
                        "flights_short_haul": {"type": "integer", "description": "short haul flights per year"},
                        "flights_long_haul": {"type": "integer", "description": "long haul flights per year"},
                        "bicycle_walking_pct": {"type": "number", "description": "percentage of trips using walking/bicycle"}
                    }
                },
                "energy": {
                    "type": "object",
                    "properties": {
                        "electricity_kwh_per_month": {"type": "number"},
                        "renewable_percentage": {"type": "number"},
                        "natural_gas": {"type": "boolean"},
                        "heating_type": {"type": "string", "description": "electric, gas, oil, heat_pump"},
                        "ac_usage_hours": {"type": "number"},
                        "household_size": {"type": "integer"}
                    }
                },
                "food": {
                    "type": "object",
                    "properties": {
                        "diet_type": {"type": "string", "description": "vegan, vegetarian, pescatarian, mixed, heavy_meat"},
                        "dairy_consumption": {"type": "string", "description": "none, low, moderate, high"},
                        "food_waste_pct": {"type": "number"},
                        "local_produce_pct": {"type": "number"}
                    }
                },
                "shopping": {
                    "type": "object",
                    "properties": {
                        "clothing_items_per_month": {"type": "integer"},
                        "electronics_per_year": {"type": "integer"},
                        "online_deliveries_per_month": {"type": "integer"},
                        "second_hand_pct": {"type": "number"}
                    }
                },
                "waste": {
                    "type": "object",
                    "properties": {
                        "recycling_frequency": {"type": "string", "description": "never, sometimes, often, always"},
                        "composting": {"type": "boolean"},
                        "plastic_usage": {"type": "string", "description": "low, moderate, high"},
                        "reusable_water_bottle": {"type": "boolean"}
                    }
                }
            }
        }
    },
    {
        "name": "recommendation_engine",
        "description": "Fetch or generate personalized sustainability recommendations to reduce carbon footprint. Call this to show the user their tailored recommendations.",
        "input_schema": {
            "type": "object",
            "properties": {
                "category": {"type": "string", "description": "Optional category filter: transportation, energy, food, shopping, waste"},
                "status": {"type": "string", "description": "Optional status filter: pending, accepted, rejected, completed"}
            }
        }
    },
    {
        "name": "ecotwin_simulator",
        "description": "Simulate lifestyle changes and compute their projected annual carbon footprint, upfront costs, and annual financial savings. Call this to run what-if simulation scenarios.",
        "input_schema": {
            "type": "object",
            "properties": {
                "scenario_name": {"type": "string", "description": "A title for the simulation scenario"},
                "changes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "category": {"type": "string", "description": "transportation, energy, food, shopping, waste"},
                            "change_type": {"type": "string", "description": "replace_vehicle, add_renewable, change_diet, reduce_waste, reduce_shopping, use_public_transport"},
                            "from_value": {"type": "string"},
                            "to_value": {"type": "string"}
                        },
                        "required": ["category", "change_type"]
                    }
                }
            },
            "required": ["scenario_name", "changes"]
        }
    },
    {
        "name": "prediction_engine",
        "description": "Predict future carbon emissions, check carbon history, reduction trends, and projected progress over time.",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "knowledge_base_retrieval",
        "description": "Retrieve verified scientific articles and guidelines from the sustainability knowledge base for any queries about carbon, emissions, global averages, and green metrics.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search term"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "sustainability_education_engine",
        "description": "Get educational articles or quizzes to learn about sustainability concepts.",
        "input_schema": {
            "type": "object",
            "properties": {
                "category": {"type": "string", "description": "e.g. food, energy, waste, transportation"}
            }
        }
    }
]


class AIService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    # ── Chat ─────────────────────────────────────────────────────

    async def chat(
        self,
        user: User,
        message: str,
        conversation_id: Optional[uuid.UUID] = None,
    ) -> ChatMessageResponse:
        """Process a user message, executing tool calls in a multi-step loop."""
        start_time = time.time()

        # Get or create conversation
        conversation = await self._get_or_create_conversation(user, conversation_id)

        # Save user message
        user_msg = Message(
            conversation_id=conversation.id,
            role="user",
            content=message,
        )
        self.db.add(user_msg)
        await self.db.flush()

        # Get user context
        context = await self._build_user_context(user, query=message)

        # Classify intent
        intent = await self._classify_intent(message)

        # Build prompt
        system = ADVISOR_PROMPT.format(user_context=json.dumps(context, default=str))

        # Get conversation history (last 10 messages)
        history = await self._get_history(conversation.id, limit=10)
        messages = []
        for m in history:
            messages.append({"role": m.role, "content": m.content})
        messages.append({"role": "user", "content": message})

        loop_count = 0
        max_loops = 5
        ai_content = ""
        tokens_used = 0

        while loop_count < max_loops:
            try:
                response = await self.client.messages.create(
                    model=settings.AI_MODEL,
                    max_tokens=settings.AI_MAX_TOKENS,
                    temperature=settings.AI_TEMPERATURE,
                    system=system,
                    messages=messages,
                    tools=AGENT_TOOLS
                )
                tokens_used += response.usage.input_tokens + response.usage.output_tokens
                
                # Check for tool call
                if response.stop_reason == "tool_use":
                    assistant_content = []
                    tool_use_blocks = []
                    for block in response.content:
                        if block.type == "text":
                            assistant_content.append({"type": "text", "text": block.text})
                        elif block.type == "tool_use":
                            assistant_content.append({
                                "type": "tool_use",
                                "id": block.id,
                                "name": block.name,
                                "input": block.input
                            })
                            tool_use_blocks.append(block)

                    messages.append({"role": "assistant", "content": assistant_content})

                    # Execute tool calls
                    tool_results = []
                    for block in tool_use_blocks:
                        result_data = await self._execute_tool(user, block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result_data, default=str)
                        })

                    messages.append({"role": "user", "content": tool_results})
                    loop_count += 1
                else:
                    ai_content = response.content[0].text
                    break
            except Exception as e:
                logger.error(f"AI API error during agent loop: {e}")
                ai_content = (
                    "I apologize, but I'm having trouble connecting to my AI service right now. "
                    "Please try again in a moment. 🙏"
                )
                break

        response_time = int((time.time() - start_time) * 1000)

        # Save final AI response
        ai_msg = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=ai_content,
            intent=intent,
            agent_used="advisor",
            tokens_used=tokens_used,
            response_time_ms=response_time,
        )
        self.db.add(ai_msg)

        # Update conversation stats
        conversation.message_count += 2
        conversation.last_intent = intent
        conversation.total_tokens_used += tokens_used
        if not conversation.title and len(message) > 5:
            conversation.title = message[:80] + ("..." if len(message) > 80 else "")

        await self.db.flush()

        # Generate suggestions
        suggestions = self._generate_suggestions(intent)

        return ChatMessageResponse(
            conversation_id=conversation.id,
            message_id=ai_msg.id,
            content=ai_content,
            intent=intent,
            agent_used="advisor",
            suggestions=suggestions,
            created_at=ai_msg.created_at,
        )

    # ── Streaming ────────────────────────────────────────────────

    async def stream_chat(
        self,
        user: User,
        message: str,
        conversation_id: Optional[uuid.UUID] = None,
    ) -> AsyncIterator[str]:
        """Stream AI response token by token via SSE, resolving tool calls in a loop."""
        conversation = await self._get_or_create_conversation(user, conversation_id)

        # Save user message
        user_msg = Message(
            conversation_id=conversation.id,
            role="user",
            content=message,
        )
        self.db.add(user_msg)
        await self.db.flush()

        context = await self._build_user_context(user, query=message)
        system = ADVISOR_PROMPT.format(user_context=json.dumps(context, default=str))

        history = await self._get_history(conversation.id, limit=10)
        messages = [{"role": m.role, "content": m.content} for m in history]
        messages.append({"role": "user", "content": message})

        loop_count = 0
        max_loops = 5
        full_response = ""
        intent = "general_chat"

        while loop_count < max_loops:
            try:
                # Call Anthropic with tools enabled
                async with self.client.messages.stream(
                    model=settings.AI_MODEL,
                    max_tokens=settings.AI_MAX_TOKENS,
                    temperature=settings.AI_TEMPERATURE,
                    system=system,
                    messages=messages,
                    tools=AGENT_TOOLS
                ) as stream:
                    # Stream text tokens directly to the user
                    async for event in stream:
                        if event.type == "text":
                            full_response += event.text
                            yield f"data: {json.dumps({'type': 'token', 'content': event.text})}\n\n"
                            
                    # Retrieve final message once stream completes
                    final_message = await stream.get_final_message()
                    
                    # Inspect if any tool calls are present
                    tool_use_blocks = [b for b in final_message.content if b.type == "tool_use"]
                    
                    if tool_use_blocks:
                        # Append assistant's message with tool calls
                        assistant_content = []
                        for b in final_message.content:
                            if b.type == "text":
                                assistant_content.append({"type": "text", "text": b.text})
                            elif b.type == "tool_use":
                                assistant_content.append({
                                    "type": "tool_use",
                                    "id": b.id,
                                    "name": b.name,
                                    "input": b.input
                                })
                        messages.append({"role": "assistant", "content": assistant_content})

                        # Execute tool calls
                        tool_results = []
                        for block in tool_use_blocks:
                            result_data = await self._execute_tool(user, block.name, block.input)
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": json.dumps(result_data, default=str)
                            })
                        
                        messages.append({"role": "user", "content": tool_results})
                        loop_count += 1
                        continue
                    else:
                        break
            except Exception as e:
                logger.error(f"AI streaming error in agent loop: {e}")
                yield f"data: {json.dumps({'type': 'error', 'content': 'AI service temporarily unavailable'})}\n\n"
                break

        # Save final complete assistant message
        ai_msg = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=full_response,
            agent_used="advisor",
        )
        self.db.add(ai_msg)
        conversation.message_count += 2
        await self.db.flush()

        yield f"data: {json.dumps({'type': 'done', 'conversation_id': str(conversation.id)})}\n\n"

    # ── Tool Executions ──────────────────────────────────────────

    async def _execute_tool(self, user: User, name: str, arguments: dict) -> dict:
        """Execute a capability tool call dynamically and return JSON serialized response."""
        logger.info(f"Agent executing tool: {name} with arguments: {arguments}")
        try:
            if name == "calculate_carbon_footprint":
                from app.services.carbon_service import CarbonService
                from app.schemas.schemas import CarbonCalculateRequest, TransportationInput, EnergyInput, FoodInput, ShoppingInput, WasteInput
                
                # Fetch inputs with defaults
                t_data = arguments.get("transportation", {})
                e_data = arguments.get("energy", {})
                f_data = arguments.get("food", {})
                s_data = arguments.get("shopping", {})
                w_data = arguments.get("waste", {})

                req = CarbonCalculateRequest(
                    transportation=TransportationInput(**t_data),
                    energy=EnergyInput(**e_data),
                    food=FoodInput(**f_data),
                    shopping=ShoppingInput(**s_data),
                    waste=WasteInput(**w_data)
                )

                service = CarbonService(self.db)
                result = await service.calculate_footprint(user.id, req)
                return result.model_dump()

            elif name == "recommendation_engine":
                from app.services.recommendation_service import RecommendationService
                service = RecommendationService(self.db)
                
                recs = await service.get_user_recommendations(
                    user.id, 
                    category=arguments.get("category"), 
                    status=arguments.get("status")
                )
                if not recs:
                    recs = await service.generate_recommendations(user.id)
                    
                return [
                    {
                        "id": str(r.id),
                        "title": r.title,
                        "description": r.description,
                        "category": r.category,
                        "difficulty": r.difficulty,
                        "estimated_co2_savings_kg": float(r.estimated_co2_savings_kg),
                        "estimated_cost_savings": float(r.estimated_cost_savings),
                        "status": r.status
                    }
                    for r in recs
                ]

            elif name == "ecotwin_simulator":
                from app.services.ecotwin_service import EcoTwinService
                from app.schemas.schemas import SimulationRequest, ScenarioChange
                
                changes = [
                    ScenarioChange(
                        category=c["category"],
                        change_type=c["change_type"],
                        from_value=c.get("from_value"),
                        to_value=c.get("to_value")
                    )
                    for c in arguments.get("changes", [])
                ]
                req = SimulationRequest(
                    scenario_name=arguments.get("scenario_name", "Simulation"),
                    changes=changes
                )
                service = EcoTwinService(self.db)
                result = await service.simulate(user.id, req)
                return result.model_dump()

            elif name == "prediction_engine":
                from app.services.carbon_service import CarbonService
                service = CarbonService(self.db)
                result = await service.get_trends(user.id)
                return {
                    "current_month_kg": result["current_month"],
                    "previous_month_kg": result["previous_month"],
                    "change_pct": result["change_pct"],
                    "trend": result["trend"]
                }

            elif name == "knowledge_base_retrieval":
                from app.services.rag_service import rag_service
                docs = await rag_service.search(arguments.get("query", ""))
                return [
                    {
                        "title": doc["title"],
                        "content": doc["content"],
                        "source": doc["source"]
                    }
                    for doc in docs
                ]

            elif name == "sustainability_education_engine":
                from app.models.extras import LearningContent
                category = arguments.get("category")
                query = select(LearningContent).where(LearningContent.is_published == True)
                if category:
                    query = query.where(LearningContent.category == category)
                
                res = await self.db.execute(query.limit(3))
                articles = res.scalars().all()
                return [
                    {
                        "title": a.title,
                        "description": a.description,
                        "category": a.category,
                        "estimated_read_time": a.estimated_read_time
                    }
                    for a in articles
                ]

            else:
                return {"error": f"Tool {name} not found"}

        except Exception as e:
            logger.error(f"Error executing tool {name}: {e}")
            return {"error": str(e)}

    # ── Conversations ────────────────────────────────────────────

    async def get_conversations(self, user_id: uuid.UUID, limit: int = 20) -> list:
        result = await self.db.execute(
            select(Conversation)
            .where(Conversation.user_id == user_id, Conversation.status == "active")
            .order_by(desc(Conversation.updated_at))
            .limit(limit)
        )
        return result.scalars().all()

    async def get_messages(self, conversation_id: uuid.UUID, user_id: uuid.UUID) -> list:
        # Verify ownership
        result = await self.db.execute(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id,
            )
        )
        conv = result.scalar_one_or_none()
        if not conv:
            raise NotFoundException("Conversation", str(conversation_id))

        result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
        )
        return result.scalars().all()

    # ── Helpers ──────────────────────────────────────────────────

    async def _get_or_create_conversation(
        self, user: User, conversation_id: Optional[uuid.UUID]
    ) -> Conversation:
        if conversation_id:
            result = await self.db.execute(
                select(Conversation).where(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user.id,
                )
            )
            conv = result.scalar_one_or_none()
            if conv:
                return conv

        conv = Conversation(user_id=user.id)
        self.db.add(conv)
        await self.db.flush()
        return conv

    async def _classify_intent(self, message: str) -> str:
        try:
            response = await self.client.messages.create(
                model=settings.AI_MODEL,
                max_tokens=50,
                temperature=0,
                system=ORCHESTRATOR_PROMPT,
                messages=[{"role": "user", "content": message}],
            )
            parsed = json.loads(response.content[0].text)
            return parsed.get("intent", "general_chat")
        except Exception:
            return "general_chat"

    async def _build_user_context(self, user: User, query: Optional[str] = None) -> dict:
        context = {
            "name": user.full_name,
            "country": user.country or "Not specified",
            "level": user.level,
            "points": user.total_points,
        }

        # Get latest carbon footprint
        result = await self.db.execute(
            select(CarbonFootprint)
            .where(CarbonFootprint.user_id == user.id)
            .order_by(desc(CarbonFootprint.created_at))
            .limit(1)
        )
        fp = result.scalar_one_or_none()
        if fp:
            context["carbon_footprint"] = {
                "monthly_kg": float(fp.monthly_kg),
                "annual_tons": float(fp.annual_tons),
                "grade": fp.grade,
                "breakdown": fp.breakdown,
            }

        # Retrieve relevant sustainability knowledge (RAG)
        if query:
            try:
                from app.services.rag_service import rag_service
                docs = await rag_service.search(query)
                context["retrieved_knowledge"] = [
                    {
                        "title": doc["title"],
                        "content": doc["content"],
                        "source": doc["source"]
                    }
                    for doc in docs
                ]
            except Exception as e:
                logger.error(f"RAG search error: {e}")

        return context

    async def _get_history(self, conversation_id: uuid.UUID, limit: int = 10) -> list:
        result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(desc(Message.created_at))
            .limit(limit)
        )
        msgs = result.scalars().all()
        return list(reversed(msgs))

    def _generate_suggestions(self, intent: str) -> List[str]:
        suggestions_map = {
            "carbon_query": [
                "How does my footprint compare to others?",
                "What's the biggest contributor?",
                "Show me my trends",
            ],
            "recommendation_request": [
                "What's the easiest change I can make?",
                "How much can I save financially?",
                "Show me the biggest impact actions",
            ],
            "eco_twin": [
                "What if I switched to an EV?",
                "Simulate going plant-based",
                "Compare solar vs wind energy",
            ],
            "education": [
                "What is carbon offsetting?",
                "Explain Scope 1, 2, 3 emissions",
                "Why does food have a carbon footprint?",
            ],
        }
        return suggestions_map.get(intent, [
            "Calculate my footprint",
            "Give me tips to reduce emissions",
            "Tell me about sustainability",
        ])
