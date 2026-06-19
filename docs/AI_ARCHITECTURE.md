# AI Agent Architecture
# FootprintIQ - AI-Powered Carbon Footprint Awareness Platform

**Version:** 1.0.0  
**Date:** June 17, 2026  
**Primary AI Model:** Claude Opus 4.5 (Anthropic)  
**Status:** Implementation Ready

---

## Table of Contents

1. [Overview](#overview)
2. [Agent Ecosystem](#agent-ecosystem)
3. [Agentic Workflow](#agentic-workflow)
4. [RAG Architecture](#rag-architecture)
5. [Agent Specifications](#agent-specifications)
6. [Tool Ecosystem](#tool-ecosystem)
7. [Prompt Engineering](#prompt-engineering)
8. [Memory & Context](#memory--context)
9. [Performance Optimization](#performance-optimization)
10. [Monitoring & Observability](#monitoring--observability)

---

## Overview

### AI-First Philosophy

FootprintIQ is built on an **AI-first architecture** where intelligent agents are the core intelligence layer, not just features. The AI system provides:

- **Intelligent Calculation:** Context-aware carbon footprint assessment
- **Personalized Coaching:** Adaptive sustainability guidance
- **Predictive Modeling:** Future emissions forecasting
- **Scenario Simulation:** What-if analysis through Eco Twin
- **Natural Conversation:** Human-like sustainability education
- **Continuous Learning:** Adaptive recommendations based on user behavior

### AI Technology Stack

```
┌─────────────────────────────────────────────────────────┐
│                  AI LAYER STACK                          │
│                                                           │
│  ┌────────────────────────────────────────────────────┐ │
│  │         Foundation Model                            │ │
│  │         Claude Opus 4.5 (Anthropic)                │ │
│  │         • 200k context window                      │ │
│  │         • Function calling                         │ │
│  │         • Vision capabilities                      │ │
│  └────────────────────────────────────────────────────┘ │
│                           ↓                              │
│  ┌────────────────────────────────────────────────────┐ │
│  │         Orchestration Layer                         │ │
│  │         LangGraph + LangChain                      │ │
│  │         • Agent workflow management                │ │
│  │         • State management                         │ │
│  │         • Tool calling                             │ │
│  └────────────────────────────────────────────────────┘ │
│                           ↓                              │
│  ┌────────────────────────────────────────────────────┐ │
│  │         Knowledge Layer                             │ │
│  │         Pinecone Vector Database                   │ │
│  │         • Semantic search                          │ │
│  │         • RAG retrieval                            │ │
│  │         • Embeddings storage                       │ │
│  └────────────────────────────────────────────────────┘ │
│                           ↓                              │
│  ┌────────────────────────────────────────────────────┐ │
│  │         Memory Layer                                │ │
│  │         Redis + PostgreSQL                         │ │
│  │         • Conversation history                     │ │
│  │         • User context                             │ │
│  │         • Agent state                              │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Key AI Capabilities

1. **Multi-Agent System:** Specialized agents for different tasks
2. **RAG-Enhanced:** Knowledge-grounded responses
3. **Tool-Augmented:** Real-world actions via tools
4. **Context-Aware:** Personalized based on user data
5. **Streaming Responses:** Real-time output generation
6. **Cost-Optimized:** Intelligent caching and prompt engineering

---

## Agent Ecosystem

### Agent Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│              ORCHESTRATOR AGENT                              │
│         (Intent Classification & Routing)                   │
│                                                              │
│  • Understands user intent                                  │
│  • Routes to appropriate specialist agent                   │
│  • Manages multi-agent coordination                         │
│  • Handles error recovery                                   │
└─────────────────────────────────────────────────────────────┘
                          ↓
        ┌─────────────────┼─────────────────┐
        ↓                 ↓                  ↓
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   CARBON     │  │   ADVISOR    │  │   ECO TWIN   │
│  ASSESSMENT  │  │    AGENT     │  │  SIMULATOR   │
│    ENGINE    │  │              │  │              │
└──────────────┘  └──────────────┘  └──────────────┘
        ↓                 ↓                  ↓
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   BEHAVIOR   │  │RECOMMENDATION│  │  PREDICTION  │
│   ANALYSIS   │  │    ENGINE    │  │    ENGINE    │
│    ENGINE    │  │              │  │              │
└──────────────┘  └──────────────┘  └──────────────┘
```

### Agent Roles & Responsibilities

| Agent | Primary Role | Key Capabilities |
|-------|--------------|------------------|
| **Orchestrator** | Intent routing | Classification, coordination, error handling |
| **Carbon Assessment Engine** | Footprint calculation | Multi-factor calculation, grading, validation |
| **Behavior Analysis Engine** | Pattern detection | Trend analysis, anomaly detection, insights |
| **Advisor Agent** | Conversational AI | Q&A, education, guidance, empathy |
| **Recommendation Engine** | Suggestion generation | Personalization, prioritization, feasibility |
| **Prediction Engine** | Forecasting | Time-series, trend projection, confidence |
| **Eco Twin Simulator** | Scenario modeling | What-if analysis, impact simulation |

---

## Agentic Workflow

### Complete User Interaction Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INPUT                                │
│  e.g., "How can I reduce my transportation emissions?"      │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              ORCHESTRATOR AGENT                              │
│                                                              │
│  Step 1: Intent Classification                              │
│  • Parse user input                                          │
│  • Identify intent: "recommendation_request"                │
│  • Detect entities: category="transportation"               │
│  • Determine complexity: "moderate"                         │
│                                                              │
│  Step 2: Context Gathering                                  │
│  • Load user profile                                         │
│  • Retrieve latest carbon footprint                         │
│  • Get transportation-specific data                         │
│  • Load conversation history                                │
│                                                              │
│  Step 3: Routing Decision                                   │
│  • Route to: Recommendation Engine                          │
│  • Supplementary: Behavior Analysis Engine                  │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│           BEHAVIOR ANALYSIS ENGINE                           │
│                                                              │
│  Step 1: Analyze Current State                              │
│  • Transportation: 1,950 kg CO2e/year (42%)                 │
│  • Primary vehicle: Petrol car, 600 km/month                │
│  • Public transport: Rarely used                            │
│  • Pattern: Daily commute 30km                              │
│                                                              │
│  Step 2: Identify Opportunities                             │
│  • High-impact area identified                              │
│  • Feasible alternatives available                          │
│  • Similar user success patterns retrieved                  │
│                                                              │
│  Output: Analysis context for Recommendation Engine         │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│           RECOMMENDATION ENGINE                              │
│                                                              │
│  Step 1: RAG Knowledge Retrieval                            │
│  • Query: "public transport recommendations commute"        │
│  • Retrieved: 5 relevant documents                          │
│  • Sources: Case studies, best practices, data             │
│                                                              │
│  Step 2: Generate Recommendations                           │
│  • Option 1: Public transport 2 days/week                   │
│    - Impact: 340 kg CO2e/year (18% reduction)               │
│    - Cost: Saves $1,800/year                                │
│    - Difficulty: Easy                                        │
│                                                              │
│  • Option 2: Carpool 3 days/week                            │
│    - Impact: 510 kg CO2e/year (26% reduction)               │
│    - Cost: Saves $1,200/year                                │
│    - Difficulty: Medium                                      │
│                                                              │
│  • Option 3: Electric vehicle                               │
│    - Impact: 1,560 kg CO2e/year (80% reduction)             │
│    - Cost: High upfront, saves $800/year long-term          │
│    - Difficulty: Hard                                        │
│                                                              │
│  Step 3: Personalization & Prioritization                   │
│  • Consider user preferences                                 │
│  • Apply feasibility filters                                │
│  • Calculate priority scores                                │
│  • Sort by impact × feasibility                             │
│                                                              │
│  Step 4: Generate Implementation Plans                      │
│  • Break down into steps                                    │
│  • Add timeline expectations                                │
│  • Include tracking metrics                                 │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              RESPONSE GENERATOR                              │
│                                                              │
│  Step 1: Format Response                                    │
│  • Structure conversational response                        │
│  • Include empathetic language                              │
│  • Add data visualizations                                  │
│  • Cite sources                                              │
│                                                              │
│  Step 2: Add Interactive Elements                           │
│  • Suggestion chips: ["Tell me more", "Compare options"]    │
│  • Action buttons: ["Accept recommendation", "Simulate"]    │
│  • Related content: ["EV buying guide", "Transit tips"]     │
│                                                              │
│  Step 3: Stream to User                                     │
│  • Token-by-token streaming                                 │
│  • Real-time rendering                                       │
│  • Progress indicators                                       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              RETURN TO USER                                  │
│                                                              │
│  "Based on your 30km daily commute, I've identified three   │
│  ways to reduce your transportation emissions...            │
│                                                              │
│  🚌 Start with public transport 2 days/week                 │
│  This is the easiest change with immediate benefits..."     │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│           POST-PROCESSING                                    │
│                                                              │
│  • Save conversation to database                            │
│  • Update user analytics                                    │
│  • Log AI metrics (tokens, latency, cost)                   │
│  • Trigger background jobs                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## RAG Architecture

### Retrieval-Augmented Generation Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                   USER QUERY                                 │
│  "Why is beef bad for the environment?"                     │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              QUERY PREPROCESSING                             │
│                                                              │
│  • Clean and normalize query                                │
│  • Extract key terms: ["beef", "environment", "impact"]     │
│  • Expand with synonyms: ["cattle", "livestock", "meat"]    │
│  • Add context: user is meat_occasional                     │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              EMBEDDING GENERATION                            │
│                                                              │
│  Model: OpenAI text-embedding-ada-002                       │
│  Input: "Why is beef bad for the environment?"              │
│  Output: Vector[1536 dimensions]                            │
│  Example: [0.023, -0.145, 0.892, ...]                       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│          VECTOR SIMILARITY SEARCH (Pinecone)                │
│                                                              │
│  Query Parameters:                                           │
│  • namespace: "sustainability_knowledge"                    │
│  • top_k: 5                                                 │
│  • similarity_metric: cosine                                │
│  • min_score: 0.7                                           │
│                                                              │
│  Filters:                                                    │
│  • category: "food"                                         │
│  • verified: true                                           │
│  • language: "en"                                           │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              RETRIEVED DOCUMENTS                             │
│                                                              │
│  Doc 1: (score: 0.92)                                       │
│  Title: "Environmental Impact of Beef Production"           │
│  Source: IPCC Report 2023                                   │
│  Content: "Beef production generates approximately 27 kg    │
│  CO2e per kg of meat, primarily due to methane emissions    │
│  from cattle digestion and land use change..."              │
│                                                              │
│  Doc 2: (score: 0.89)                                       │
│  Title: "Livestock and Climate Change"                      │
│  Source: FAO Study 2024                                     │
│  Content: "The livestock sector accounts for 14.5% of       │
│  global greenhouse gas emissions. Beef and dairy cattle     │
│  are responsible for 65% of this..."                        │
│                                                              │
│  Doc 3: (score: 0.85)                                       │
│  Title: "Sustainable Protein Alternatives"                  │
│  Source: Nature Sustainability                              │
│  Content: "Replacing beef with plant-based proteins can     │
│  reduce food-related emissions by up to 70%..."             │
│                                                              │
│  [+ 2 more documents]                                       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              CONTEXT AUGMENTATION                            │
│                                                              │
│  Combine:                                                    │
│  1. Retrieved knowledge documents                           │
│  2. User profile data (diet: meat_occasional)               │
│  3. User's carbon footprint (food: 840 kg/year)             │
│  4. Conversation history (past 5 messages)                  │
│  5. User preferences (learning style: visual)               │
│                                                              │
│  Total context: ~8,000 tokens                               │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              PROMPT CONSTRUCTION                             │
│                                                              │
│  System Prompt: [Agent personality and instructions]        │
│  +                                                           │
│  Retrieved Context: [Knowledge documents]                   │
│  +                                                           │
│  User Context: [Profile and history]                        │
│  +                                                           │
│  User Query: "Why is beef bad for the environment?"         │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│         CLAUDE OPUS 4.5 GENERATION                           │
│                                                              │
│  Configuration:                                              │
│  • temperature: 0.7                                          │
│  • max_tokens: 1000                                          │
│  • top_p: 0.9                                               │
│  • stream: true                                             │
│                                                              │
│  Processing:                                                 │
│  • Analyze augmented context                                │
│  • Generate factual, grounded response                      │
│  • Include specific citations                               │
│  • Personalize for user                                     │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              POST-PROCESSING                                 │
│                                                              │
│  • Format citations: [Source: IPCC 2023]                    │
│  • Add visual elements (if applicable)                      │
│  • Extract action items                                     │
│  • Generate follow-up suggestions                           │
│  • Validate factual accuracy                                │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              RETURN TO USER                                  │
│                                                              │
│  "Beef production has a significant environmental impact    │
│  for three main reasons:                                    │
│                                                              │
│  1. **Methane Emissions**: Cattle produce ~27 kg CO2e per   │
│     kg of beef through digestion [IPCC 2023]                │
│                                                              │
│  2. **Land Use**: Requires 20x more land than plant         │
│     proteins [FAO 2024]                                     │
│                                                              │
│  3. **Resource Intensive**: High water and feed needs       │
│                                                              │
│  Since you're an occasional meat eater, reducing beef to    │
│  once weekly could cut your food emissions by 15%..."       │
└─────────────────────────────────────────────────────────────┘
```

### Knowledge Base Structure

#### Vector Database Collections

**1. Sustainability Knowledge Base**
```
Collection: sustainability_knowledge
Namespace: general

Documents: 50,000+
Embedding Model: text-embedding-ada-002
Dimensions: 1536

Content Types:
- Scientific papers and research
- Climate science facts
- Carbon calculation methodologies
- Environmental impact data
- Industry standards

Metadata Schema:
{
  "id": "doc_12345",
  "source": "IPCC AR6 Report",
  "category": "climate_science",
  "subcategory": "emissions",
  "verified": true,
  "publication_date": "2023-04-15",
  "author": "IPCC",
  "confidence": 0.98,
  "language": "en",
  "tags": ["ghg", "carbon", "methodology"]
}
```

**2. Recommendation Library**
```
Collection: recommendations
Namespace: strategies

Documents: 10,000+

Content Types:
- Proven reduction strategies
- Case studies and success stories
- Implementation guides
- Best practices
- Common pitfalls and solutions

Metadata Schema:
{
  "id": "rec_456",
  "category": "transportation",
  "impact_level": "high",
  "difficulty": "medium",
  "cost": "saves_money",
  "success_rate": 0.78,
  "avg_co2_saved_kg": 450,
  "region": "global",
  "verified": true
}
```

**3. Educational Content**
```
Collection: education
Namespace: learning

Documents: 25,000+

Content Types:
- Sustainability concepts
- Carbon terminology definitions
- How-to guides
- FAQs
- Explainer articles

Metadata Schema:
{
  "id": "edu_789",
  "topic": "carbon_offsetting",
  "difficulty": "beginner",
  "content_type": "explainer",
  "estimated_read_time": 5,
  "prerequisites": [],
  "related_topics": ["carbon_neutral", "emissions"]
}
```

**4. Behavioral Patterns**
```
Collection: patterns
Namespace: user_behavior

Documents: 100,000+ (anonymized)

Content Types:
- Successful transition patterns
- Common challenges
- Solution patterns
- Demographic insights

Metadata Schema:
{
  "id": "pattern_101",
  "transition_type": "car_to_public_transport",
  "success_indicators": ["consistency", "route_planning"],
  "timeline_weeks": 4,
  "dropout_rate": 0.15,
  "demographic": "urban_professional"
}
```

### RAG Performance Optimization

**1. Semantic Caching**
```python
# Cache frequently asked questions
query_embedding = embed("What is carbon footprint?")
cache_key = f"rag_cache:{hash(query_embedding)}"

if redis.exists(cache_key):
    return redis.get(cache_key)
else:
    result = perform_rag(query)
    redis.setex(cache_key, 3600, result)  # 1 hour TTL
    return result
```

**2. Hybrid Search**
```python
# Combine vector search with keyword matching
vector_results = pinecone.query(
    vector=query_embedding,
    top_k=10,
    filter={"category": "food"}
)

keyword_results = elasticsearch.search(
    query=user_query,
    index="sustainability_docs"
)

# Merge and re-rank
final_results = merge_and_rerank(vector_results, keyword_results)
```

**3. Dynamic Top-K**
```python
# Adjust retrieval based on query complexity
if query_complexity == "simple":
    top_k = 3
elif query_complexity == "moderate":
    top_k = 5
else:  # complex
    top_k = 10
```

---

## Agent Specifications

### 1. Orchestrator Agent

**Purpose:** Intent classification and agent routing

**System Prompt:**
```
You are the Orchestrator Agent for FootprintIQ, a sustainability platform.

Your role:
1. Analyze user inputs to determine intent
2. Route queries to appropriate specialist agents
3. Coordinate multi-agent workflows
4. Handle ambiguous or complex requests

Intent Categories:
- carbon_calculation: User wants to calculate footprint
- recommendation_request: User wants reduction suggestions
- information_query: User has questions
- eco_twin_simulation: User wants scenario analysis
- general_conversation: Casual sustainability chat

Always respond with structured routing decisions.
```

**Input Schema:**
```json
{
  "user_message": "string",
  "user_context": {
    "user_id": "uuid",
    "has_footprint": "boolean",
    "conversation_history": "array"
  }
}
```

**Output Schema:**
```json
{
  "intent": "recommendation_request",
  "confidence": 0.95,
  "entities": {
    "category": "transportation",
    "urgency": "medium"
  },
  "routing_decision": {
    "primary_agent": "recommendation_engine",
    "supporting_agents": ["behavior_analysis"],
    "execution_mode": "sequential"
  },
  "context_needed": ["carbon_footprint", "transportation_data"]
}
```

---

### 2. Carbon Assessment Engine

**Purpose:** Calculate carbon footprints with high accuracy

**System Prompt:**
```
You are the Carbon Assessment Engine for FootprintIQ.

Your responsibilities:
1. Calculate carbon footprints based on user inputs
2. Apply scientifically-validated emission factors
3. Assign sustainability grades
4. Provide category-wise breakdowns
5. Compare against benchmarks

Use the provided calculation tools and emission factor database.
Always cite methodology sources.
Flag any data quality issues or assumptions.
```

**Calculation Tools:**

```python
@tool
def calculate_transportation_emissions(
    vehicle_type: str,
    km_per_month: int,
    fuel_type: Optional[str] = None
) -> dict:
    """Calculate transportation emissions"""
    emission_factors = {
        "car_petrol": 0.171,  # kg CO2e per km
        "car_diesel": 0.176,
        "ev": 0.053,
        "motorcycle": 0.113,
        "bus": 0.089,
        "train": 0.041
    }
    
    factor = emission_factors.get(vehicle_type, 0)
    monthly_kg = km_per_month * factor
    annual_kg = monthly_kg * 12
    
    return {
        "monthly_kg": round(monthly_kg, 2),
        "annual_kg": round(annual_kg, 2),
        "emission_factor": factor
    }
```

**Grading Algorithm:**
```python
def assign_grade(annual_tons: float) -> dict:
    """Assign sustainability grade"""
    if annual_tons < 2.0:
        return {"grade": "EXCELLENT", "score": 95, "color": "#10B981"}
    elif annual_tons < 4.0:
        return {"grade": "GOOD", "score": 75, "color": "#34D399"}
    elif annual_tons < 6.0:
        return {"grade": "MODERATE", "score": 55, "color": "#FBBF24"}
    elif annual_tons < 10.0:
        return {"grade": "HIGH", "score": 35, "color": "#F97316"}
    else:
        return {"grade": "CRITICAL", "score": 15, "color": "#EF4444"}
```

---

### 3. Advisor Agent

**Purpose:** Conversational AI for sustainability guidance

**System Prompt:**
```
You are the FootprintIQ Sustainability Advisor, a friendly and knowledgeable AI coach.

Personality Traits:
- Warm and approachable
- Educational but not preachy
- Encouraging and positive
- Data-driven and factual
- Non-judgmental
- Solution-oriented

Communication Style:
- Use "I" and "you" for personal connection
- Include relevant data and statistics
- Provide actionable next steps
- Ask clarifying questions when needed
- Celebrate user progress

Knowledge Areas:
- Carbon footprints and climate science
- Sustainable living practices
- Behavior change psychology
- Cost-benefit analysis
- Regional variations

Always:
1. Ground responses in retrieved knowledge
2. Cite sources for statistics
3. Personalize based on user context
4. Offer multiple options when relevant
5. End with actionable next steps
```

**Conversation Examples:**

**Example 1: Educational Query**
```
User: "What's the difference between carbon neutral and net zero?"

Advisor: "Great question! These terms are often confused.

**Carbon Neutral** means balancing CO2 emissions by offsetting—for example, planting trees or buying carbon credits to compensate for emissions you can't eliminate [Carbon Trust 2024].

**Net Zero** is more ambitious. It means reducing emissions as much as possible (typically 90%+) and only offsetting what truly can't be eliminated [IPCC 2023].

Think of it this way:
- Carbon Neutral: "I'll drive but plant trees"
- Net Zero: "I'll bike most days and offset rare unavoidable trips"

Your current footprint is 4.64 tons CO2e annually. A net-zero target would mean reducing to under 0.5 tons—achievable through public transport, plant-based diet, and renewable energy!

Want to see what your net-zero path could look like?"

Suggested actions:
• Explore your Eco Twin scenarios
• See net-zero roadmap
• Learn about carbon offsetting
```

**Example 2: Recommendation Request**
```
User: "How can I reduce my emissions?"

Advisor: "I've analyzed your carbon profile, and I have good news—you have some high-impact opportunities!

Your biggest contributor is transportation at 42% (1.95 tons/year). Based on your 30km daily commute, here are three strategies:

🚌 **Quick Win: Public Transport 2 Days/Week**
- Impact: 340 kg CO2e saved/year (18% reduction)
- Cost: Saves $1,800/year
- Difficulty: Easy
- Timeline: Start this week

This is perfect for Tuesday/Thursday when traffic is lighter. You'll reduce emissions AND save money!

🚗 **Medium-Term: Carpool 3 Days/Week**
- Impact: 510 kg saved/year (26% reduction)
- Uses your existing car
- Social benefit of sharing rides

⚡ **Long-Term: Electric Vehicle**
- Impact: 1,560 kg saved/year (80% reduction)
- Higher upfront cost but long-term savings
- Best for frequent drivers

I recommend starting with option 1 while researching option 3 for next year. Ready to create an action plan?"
```

---

### 4. Recommendation Engine

**Purpose:** Generate personalized sustainability recommendations

**System Prompt:**
```
You are the Recommendation Engine for FootprintIQ.

Generate personalized, actionable recommendations by:

1. **Analyzing User Data:**
   - Current carbon footprint and breakdown
   - Historical behavior patterns
   - Demographic information
   - Stated preferences and goals

2. **Retrieving Knowledge:**
   - Proven strategies from knowledge base
   - Similar user success patterns
   - Regional best practices
   - Cost-benefit data

3. **Generating Recommendations:**
   - Specific and measurable
   - Prioritized by impact × feasibility
   - Include implementation steps
   - Quantify expected savings
   - Provide realistic timelines

4. **Personalization Factors:**
   - Current lifestyle constraints
   - Financial situation
   - Geographic location
   - Past acceptance patterns
   - Difficulty preference

Output Format:
- Title (action-oriented)
- Description (why it matters)
- Impact metrics (CO2 and financial)
- Difficulty and timeline
- Step-by-step implementation
- Tracking metrics
```

**Prioritization Formula:**
```python
def calculate_priority_score(recommendation: dict, user: dict) -> int:
    """
    Calculate recommendation priority (0-100)
    """
    # Impact score (0-40 points)
    impact_score = min(40, (recommendation['co2_savings_kg'] / 1000) * 10)
    
    # Feasibility score (0-30 points)
    difficulty_map = {"easy": 30, "medium": 20, "hard": 10}
    feasibility_score = difficulty_map.get(recommendation['difficulty'], 15)
    
    # Cost benefit (0-20 points)
    if recommendation['estimated_cost'] < 0:  # Saves money
        cost_score = 20
    elif recommendation['estimated_cost'] == 0:
        cost_score = 10
    else:
        cost_score = 5
    
    # Personalization (0-10 points)
    personalization_score = calculate_user_fit(recommendation, user)
    
    total = impact_score + feasibility_score + cost_score + personalization_score
    return min(100, int(total))
```

---

### 5. Prediction Engine

**Purpose:** Forecast future emissions and trends

**System Prompt:**
```
You are the Prediction Engine for FootprintIQ.

Responsibilities:
1. Forecast future carbon emissions (30/90/365 days)
2. Identify trends and patterns
3. Predict behavior change impact
4. Provide confidence intervals
5. Generate early warnings

Methodology:
- Time series analysis of historical data
- Behavioral pattern recognition
- Seasonal adjustment
- Trend extrapolation
- Monte Carlo simulation for uncertainty

Always provide:
- Point estimates
- Confidence intervals (80%, 95%)
- Assumptions made
- Factors that could change forecast
- Recommended actions based on prediction
```

**Forecasting Models:**
```python
class EmissionsForecast:
    def predict_30_day(self, user_history: List[dict]) -> dict:
        """30-day emissions forecast"""
        # Extract recent trend
        recent_data = user_history[-90:]  # Last 90 days
        
        # Calculate moving average
        ma_30 = calculate_moving_average(recent_data, window=30)
        
        # Detect trend (increasing/decreasing/stable)
        trend = detect_trend(ma_30)
        
        # Extrapolate
        prediction = extrapolate_linear(ma_30, days=30)
        
        # Add confidence intervals
        std_dev = calculate_std_dev(recent_data)
        ci_80 = (prediction - std_dev, prediction + std_dev)
        ci_95 = (prediction - 2*std_dev, prediction + 2*std_dev)
        
        return {
            "prediction_kg": round(prediction, 2),
            "confidence_80": ci_80,
            "confidence_95": ci_95,
            "trend": trend,
            "confidence_score": 0.85
        }
```

---

### 6. Eco Twin Simulator

**Purpose:** Simulate what-if scenarios for lifestyle changes

**System Prompt:**
```
You are the Eco Twin Simulator, FootprintIQ's flagship innovation feature.

Capabilities:
1. Create virtual sustainability twins
2. Simulate lifestyle change scenarios
3. Compare multiple scenarios side-by-side
4. Calculate long-term impacts
5. Provide feasibility analysis

Simulation Process:
1. Establish baseline (current state)
2. Apply proposed changes
3. Calculate new emissions
4. Compute reduction and impact
5. Estimate costs and timeline
6. Assess feasibility and risks

Output Format:
- Scenario name and description
- Changes applied
- New annual footprint
- Reduction (tons and %)
- Financial impact
- Timeline to implement
- Difficulty score
- Risk factors
```

**Simulation Engine:**
```python
class EcoTwinSimulator:
    def simulate_scenario(
        self,
        baseline: CarbonFootprint,
        changes: List[Change]
    ) -> SimulationResult:
        """
        Simulate a what-if scenario
        
        Args:
            baseline: Current carbon footprint
            changes: List of proposed changes
        
        Returns:
            Simulation results with impacts
        """
        new_footprint = copy.deepcopy(baseline)
        total_cost = 0
        implementation_time = 0
        
        for change in changes:
            # Apply change to footprint
            impact = self._calculate_change_impact(change)
            new_footprint.apply_impact(impact)
            
            # Accumulate costs and time
            total_cost += change.estimated_cost
            implementation_time = max(implementation_time, change.time_weeks)
        
        # Calculate reductions
        reduction_tons = baseline.annual_tons - new_footprint.annual_tons
        reduction_pct = (reduction_tons / baseline.annual_tons) * 100
        
        # Assess feasibility
        feasibility = self._assess_feasibility(changes, user_context)
        
        return SimulationResult(
            scenario_name=generate_name(changes),
            new_footprint=new_footprint,
            reduction_tons=reduction_tons,
            reduction_percentage=reduction_pct,
            estimated_cost=total_cost,
            implementation_weeks=implementation_time,
            feasibility_score=feasibility,
            risk_factors=self._identify_risks(changes)
        )
```

**Pre-built Scenarios:**
```python
SCENARIOS = {
    "go_fully_electric": {
        "name": "Go Fully Electric",
        "changes": [
            {"category": "transportation", "action": "replace_car_with_ev"},
            {"category": "energy", "action": "install_solar_panels"}
        ],
        "expected_reduction_pct": 65,
        "difficulty": "hard",
        "cost_range": "$30,000-$50,000"
    },
    "plant_based_diet": {
        "name": "Plant-Based Diet",
        "changes": [
            {"category": "food", "action": "switch_to_vegan"}
        ],
        "expected_reduction_pct": 15,
        "difficulty": "medium",
        "cost_range": "Neutral to saves money"
    },
    "zero_waste_lifestyle": {
        "name": "Zero Waste Lifestyle",
        "changes": [
            {"category": "waste", "action": "eliminate_single_use"},
            {"category": "shopping", "action": "buy_only_second_hand"}
        ],
        "expected_reduction_pct": 8,
        "difficulty": "medium",
        "cost_range": "Saves $1,000/year"
    }
}
```

---

## Tool Ecosystem

### Available Tools for Agents

```python
from langchain.tools import tool

@tool
def calculate_carbon_footprint(data: dict) -> dict:
    """Calculate complete carbon footprint from input data"""
    pass

@tool
def query_knowledge_base(query: str, category: str = None) -> List[dict]:
    """Search sustainability knowledge base"""
    pass

@tool
def get_user_context(user_id: str) -> dict:
    """Retrieve complete user context"""
    pass

@tool
def get_carbon_history(user_id: str, days: int = 90) -> List[dict]:
    """Get historical carbon footprint data"""
    pass

@tool
def generate_recommendation(
    user_id: str,
    category: str,
    priority: str = "high"
) -> dict:
    """Generate personalized recommendation"""
    pass

@tool
def simulate_scenario(
    baseline_id: str,
    changes: List[dict]
) -> dict:
    """Run Eco Twin simulation"""
    pass

@tool
def get_similar_users(user_id: str, limit: int = 10) -> List[dict]:
    """Find users with similar profiles"""
    pass

@tool
def calculate_impact(
    current: float,
    proposed: float,
    category: str
) -> dict:
    """Calculate impact of a change"""
    pass

@tool
def get_regional_data(country_code: str) -> dict:
    """Get region-specific data and averages"""
    pass

@tool
def track_recommendation(
    recommendation_id: str,
    action: str
) -> dict:
    """Track user action on recommendation"""
    pass
```

---

## Prompt Engineering

### System Prompt Template

```python
SYSTEM_PROMPT_TEMPLATE = """
You are {agent_name}, an AI agent in the FootprintIQ sustainability platform.

## Your Role
{role_description}

## Core Capabilities
{capabilities}

## Communication Guidelines
1. Be warm, friendly, and encouraging
2. Use data to support recommendations
3. Provide actionable next steps
4. Celebrate user progress
5. Never be judgmental
6. Cite sources for statistics

## Context Awareness
You have access to:
- User's carbon footprint: {carbon_footprint}
- User profile: {user_profile}
- Conversation history: {conversation_history}
- Retrieved knowledge: {rag_context}

## Output Format
{output_format}

## Important Constraints
- Never make up statistics
- Always cite sources
- Flag assumptions clearly
- Respect user privacy
- Be transparent about limitations

Current date: {current_date}
"""
```

### Few-Shot Examples

```python
FEW_SHOT_EXAMPLES = [
    {
        "user": "How much CO2 does a flight from New York to London produce?",
        "assistant": "A round-trip flight from New York to London generates approximately 1.6 tons CO2e per passenger [ICAO Carbon Calculator 2024]. \n\nTo put this in perspective:\n- That's equivalent to driving 9,400 km in a petrol car\n- Or 34% of the average American's annual footprint\n- It would take 73 trees one year to offset this\n\nIf you need to fly, consider:\n✈️ Choose direct flights (20-30% less emissions)\n💺 Fly economy (business class = 3x more emissions)\n🌳 Purchase quality carbon offsets\n🚂 Consider train for shorter distances\n\nWould you like help finding lower-emission alternatives for your trip?"
    },
    {
        "user": "I feel bad about my high footprint",
        "assistant": "I appreciate your awareness—that's actually the first step to positive change! 🌱\n\nLet me share something important: Your current footprint of 8.2 tons is above average, but you're already taking action by using FootprintIQ. Most people don't even measure their impact.\n\nHere's the good news:\n1. You have significant reduction opportunities\n2. Small changes can have big impacts\n3. You're not alone—our community is here\n\nLet's focus on progress, not perfection. I've identified 3 easy changes that could reduce your footprint by 25% in the next 3 months.\n\nReady to see them? 🎯"
    }
]
```

### Dynamic Prompting

```python
def build_dynamic_prompt(
    agent_type: str,
    user_context: dict,
    query: str,
    rag_results: List[dict]
) -> str:
    """Build context-aware prompt"""
    
    # Base system prompt
    system = get_system_prompt(agent_type)
    
    # Add user context
    if user_context.get("carbon_footprint"):
        system += f"\n\nUser's current footprint: {user_context['carbon_footprint']['annual_tons']} tons CO2e/year"
    
    # Add retrieved knowledge
    if rag_results:
        knowledge = "\n\n## Retrieved Knowledge:\n"
        for doc in rag_results[:3]:
            knowledge += f"\n[{doc['source']}]: {doc['content'][:500]}...\n"
        system += knowledge
    
    # Add conversation history
    if user_context.get("history"):
        history = "\n\n## Recent Conversation:\n"
        for msg in user_context["history"][-3:]:
            history += f"{msg['role']}: {msg['content']}\n"
        system += history
    
    return system
```

---

## Memory & Context

### Conversation Memory

```python
class ConversationMemory:
    """Manage conversation context and history"""
    
    def __init__(self, redis_client, db_session):
        self.redis = redis_client
        self.db = db_session
    
    async def get_conversation_context(
        self,
        conversation_id: str,
        max_messages: int = 10
    ) -> dict:
        """
        Retrieve conversation context
        
        Includes:
        - Recent messages
        - User profile
        - Carbon footprint data
        - Active recommendations
        """
        # Try cache first
        cache_key = f"conv:{conversation_id}:context"
        cached = await self.redis.get(cache_key)
        if cached:
            return json.loads(cached)
        
        # Build context from database
        messages = await self._get_messages(conversation_id, max_messages)
        user = await self._get_user(conversation_id)
        footprint = await self._get_latest_footprint(user.id)
        recommendations = await self._get_active_recommendations(user.id)
        
        context = {
            "messages": messages,
            "user_profile": user.to_dict(),
            "carbon_footprint": footprint.to_dict() if footprint else None,
            "recommendations": [r.to_dict() for r in recommendations]
        }
        
        # Cache for 5 minutes
        await self.redis.setex(cache_key, 300, json.dumps(context))
        
        return context
    
    async def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        metadata: dict = None
    ):
        """Add message and update context"""
        # Save to database
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            metadata=metadata
        )
        self.db.add(message)
        await self.db.commit()
        
        # Invalidate cache
        cache_key = f"conv:{conversation_id}:context"
        await self.redis.delete(cache_key)
        
        # Update conversation summary
        await self._update_conversation_summary(conversation_id)
```

### User Context Management

```python
class UserContextManager:
    """Manage user-specific context for AI agents"""
    
    async def get_full_context(self, user_id: str) -> dict:
        """
        Get comprehensive user context
        
        Returns:
        - Profile information
        - Carbon footprint history
        - Behavioral patterns
        - Preferences
        - Active goals
        - Recommendation history
        """
        return {
            "profile": await self._get_profile(user_id),
            "carbon_data": await self._get_carbon_data(user_id),
            "behavior_patterns": await self._analyze_patterns(user_id),
            "preferences": await self._get_preferences(user_id),
            "goals": await self._get_goals(user_id),
            "recommendation_history": await self._get_rec_history(user_id),
            "gamification": await self._get_gamification(user_id)
        }
```

---

## Performance Optimization

### Response Streaming

```python
async def stream_ai_response(
    prompt: str,
    user_id: str
) -> AsyncIterator[str]:
    """Stream AI response token by token"""
    
    async with anthropic.AsyncAnthropic() as client:
        async with client.messages.stream(
            model="claude-opus-4.5",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.7
        ) as stream:
            async for text in stream.text_stream:
                yield text
                
                # Send to frontend via WebSocket
                await websocket_manager.send(user_id, {
                    "type": "ai_token",
                    "content": text
                })
```

### Prompt Caching

```python
# Cache common prompts
@lru_cache(maxsize=1000)
def get_cached_prompt(prompt_type: str, **kwargs) -> str:
    """Cache frequently used prompts"""
    return PROMPT_TEMPLATES[prompt_type].format(**kwargs)
```

### Batch Processing

```python
async def batch_generate_recommendations(
    user_ids: List[str]
) -> dict:
    """Generate recommendations for multiple users efficiently"""
    
    # Gather all user contexts
    contexts = await asyncio.gather(*[
        get_user_context(uid) for uid in user_ids
    ])
    
    # Batch RAG retrieval
    rag_results = await batch_rag_query([
        f"recommendations for {ctx['profile']['diet']}" 
        for ctx in contexts
    ])
    
    # Generate recommendations
    recommendations = await asyncio.gather(*[
        generate_recommendation(ctx, rag)
        for ctx, rag in zip(contexts, rag_results)
    ])
    
    return dict(zip(user_ids, recommendations))
```

---

## Monitoring & Observability

### LangSmith Integration

```python
from langsmith import Client
from langsmith.run_helpers import traceable

langsmith_client = Client()

@traceable(
    run_type="llm",
    name="carbon_calculation",
    project_name="footprintiq-production"
)
async def calculate_with_ai(input_data: dict) -> dict:
    """Traced AI calculation"""
    result = await carbon_engine.calculate(input_data)
    return result
```

### Key Metrics

```python
AI_METRICS = {
    "request_metrics": [
        "total_requests",
        "requests_by_agent",
        "requests_by_intent",
        "success_rate",
        "error_rate"
    ],
    "performance_metrics": [
        "average_latency",
        "p95_latency",
        "p99_latency",
        "tokens_per_request",
        "cost_per_request"
    ],
    "quality_metrics": [
        "user_rating",
        "conversation_length",
        "recommendation_acceptance_rate",
        "simulation_usage"
    ],
    "rag_metrics": [
        "retrieval_latency",
        "document_relevance",
        "cache_hit_rate",
        "average_docs_retrieved"
    ]
}
```

### Alert Conditions

```python
ALERT_CONDITIONS = {
    "high_latency": {
        "condition": "p95_latency > 5000ms",
        "severity": "warning"
    },
    "high_error_rate": {
        "condition": "error_rate > 5%",
        "severity": "critical"
    },
    "high_cost": {
        "condition": "hourly_cost > $50",
        "severity": "warning"
    },
    "low_quality": {
        "condition": "average_rating < 3.5",
        "severity": "warning"
    }
}
```

---

## Cost Management

### Token Optimization

```python
def optimize_prompt(prompt: str, max_tokens: int = 4000) -> str:
    """Optimize prompt to reduce token usage"""
    
    # Remove unnecessary whitespace
    prompt = re.sub(r'\s+', ' ', prompt)
    
    # Truncate long contexts
    if count_tokens(prompt) > max_tokens:
        prompt = truncate_to_tokens(prompt, max_tokens)
    
    return prompt

def count_tokens(text: str) -> int:
    """Estimate token count"""
    # Rough estimate: 1 token ≈ 4 characters
    return len(text) // 4
```

### Cost Tracking

```python
class CostTracker:
    """Track AI API costs"""
    
    PRICING = {
        "claude-opus-4.5": {
            "input": 0.015,  # per 1K tokens
            "output": 0.075  # per 1K tokens
        }
    }
    
    async def track_request(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """Calculate and track cost"""
        
        pricing = self.PRICING[model]
        cost = (
            (input_tokens / 1000) * pricing["input"] +
            (output_tokens / 1000) * pricing["output"]
        )
        
        # Log to database
        await self.log_cost(model, cost, input_tokens, output_tokens)
        
        # Update metrics
        await self.update_metrics(cost)
        
        return cost
```

---

## Security & Safety

### Content Filtering

```python
async def filter_content(text: str) -> dict:
    """Filter inappropriate content"""
    
    # Check for PII
    if contains_pii(text):
        return {
            "allowed": False,
            "reason": "Contains personal identifiable information"
        }
    
    # Check for harmful content
    if contains_harmful_content(text):
        return {
            "allowed": False,
            "reason": "Contains harmful content"
        }
    
    return {"allowed": True}
```

### Rate Limiting

```python
class AIRateLimiter:
    """Rate limit AI requests per user"""
    
    async def check_limit(self, user_id: str) -> bool:
        """Check if user is within rate limits"""
        
        key = f"ai_rate:{user_id}"
        current = await redis.get(key)
        
        if current and int(current) >= MAX_REQUESTS_PER_HOUR:
            return False
        
        # Increment counter
        await redis.incr(key)
        await redis.expire(key, 3600)  # 1 hour
        
        return True
```

---

**Document Owner:** AI/ML Architect  
**Last Updated:** June 17, 2026  
**Next Review:** July 17, 2026  
**Status:** APPROVED FOR IMPLEMENTATION
