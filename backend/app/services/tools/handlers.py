"""
AI Tool Execution Handlers.
Implements the logic for each tool and registers them with the ToolRegistry.
"""

from typing import Any, Dict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.services.tools.registry import registry


# ── Calculate Carbon Footprint ───────────────────────────────────

CALCULATE_CARBON_SCHEMA = {
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
}

async def handle_calculate_carbon(db: AsyncSession, user: User, arguments: Dict[str, Any]) -> Dict[str, Any]:
    from app.services.carbon_service import CarbonService
    from app.schemas.schemas import CarbonCalculateRequest, TransportationInput, EnergyInput, FoodInput, ShoppingInput, WasteInput
    
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

    service = CarbonService(db)
    result = await service.calculate_footprint(user.id, req)
    return result.model_dump()


# ── Recommendation Engine ────────────────────────────────────────

RECOMMENDATION_SCHEMA = {
    "description": "Fetch or generate personalized sustainability recommendations to reduce carbon footprint. Call this to show the user their tailored recommendations.",
    "input_schema": {
        "type": "object",
        "properties": {
            "category": {"type": "string", "description": "Optional category filter: transportation, energy, food, shopping, waste"},
            "status": {"type": "string", "description": "Optional status filter: pending, accepted, rejected, completed"}
        }
    }
}

async def handle_recommendation(db: AsyncSession, user: User, arguments: Dict[str, Any]) -> Any:
    from app.services.recommendation_service import RecommendationService
    service = RecommendationService(db)
    
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


# ── Eco Twin Simulator ───────────────────────────────────────────

ECOTWIN_SCHEMA = {
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
}

async def handle_ecotwin(db: AsyncSession, user: User, arguments: Dict[str, Any]) -> Dict[str, Any]:
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
    service = EcoTwinService(db)
    result = await service.simulate(user.id, req)
    return result.model_dump()


# ── Prediction Engine ────────────────────────────────────────────

PREDICTION_SCHEMA = {
    "description": "Predict future carbon emissions, check carbon history, reduction trends, and projected progress over time.",
    "input_schema": {
        "type": "object",
        "properties": {}
    }
}

async def handle_prediction(db: AsyncSession, user: User, arguments: Dict[str, Any]) -> Dict[str, Any]:
    from app.services.carbon_service import CarbonService
    service = CarbonService(db)
    result = await service.get_trends(user.id)
    return {
        "current_month_kg": result["current_month"],
        "previous_month_kg": result["previous_month"],
        "change_pct": result["change_pct"],
        "trend": result["trend"]
    }


# ── Knowledge Base Retrieval ─────────────────────────────────────

KNOWLEDGE_SCHEMA = {
    "description": "Retrieve verified scientific articles and guidelines from the sustainability knowledge base for any queries about carbon, emissions, global averages, and green metrics.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "The search term"}
        },
        "required": ["query"]
    }
}

async def handle_knowledge(db: AsyncSession, user: User, arguments: Dict[str, Any]) -> Any:
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


# ── Sustainability Education ─────────────────────────────────────

EDUCATION_SCHEMA = {
    "description": "Get educational articles or quizzes to learn about sustainability concepts.",
    "input_schema": {
        "type": "object",
        "properties": {
            "category": {"type": "string", "description": "e.g. food, energy, waste, transportation"}
        }
    }
}

async def handle_education(db: AsyncSession, user: User, arguments: Dict[str, Any]) -> Any:
    from app.models.extras import LearningContent
    category = arguments.get("category")
    query = select(LearningContent).where(LearningContent.is_published == True)
    if category:
        query = query.where(LearningContent.category == category)
    
    res = await db.execute(query.limit(3))
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


# ── Register all tools ───────────────────────────────────────────

def register_all_tools():
    """Register all available AI tools with the registry."""
    registry.register("calculate_carbon_footprint", CALCULATE_CARBON_SCHEMA, handle_calculate_carbon)
    registry.register("recommendation_engine", RECOMMENDATION_SCHEMA, handle_recommendation)
    registry.register("ecotwin_simulator", ECOTWIN_SCHEMA, handle_ecotwin)
    registry.register("prediction_engine", PREDICTION_SCHEMA, handle_prediction)
    registry.register("knowledge_base_retrieval", KNOWLEDGE_SCHEMA, handle_knowledge)
    registry.register("sustainability_education_engine", EDUCATION_SCHEMA, handle_education)

# Execute registration on module load
register_all_tools()
