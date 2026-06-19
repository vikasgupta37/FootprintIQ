"""
Eco Twin Service — scenario simulation and prediction engine.
"""

import copy
import time
from decimal import Decimal
from typing import Dict, List, Optional
from uuid import UUID

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException
from app.models.carbon import CarbonFootprint
from app.models.extras import EcoTwinSimulation, EcoTwinState
from app.schemas.schemas import SimulationRequest, SimulationResponse


# Pre-built scenario definitions
PREBUILT_SCENARIOS = {
    "go_fully_electric": {
        "id": "scenario_ev",
        "name": "Go Fully Electric",
        "description": "Switch to an electric vehicle and install solar panels",
        "expected_reduction_pct": 65,
        "difficulty": "hard",
        "estimated_cost": "$40,000 – $60,000",
    },
    "plant_based_diet": {
        "id": "scenario_plant_based",
        "name": "Plant-Based Diet",
        "description": "Switch to a fully plant-based (vegan) diet",
        "expected_reduction_pct": 15,
        "difficulty": "medium",
        "estimated_cost": "Neutral to saves money",
    },
    "zero_waste_lifestyle": {
        "id": "scenario_zero_waste",
        "name": "Zero Waste Lifestyle",
        "description": "Eliminate single-use plastics and buy second-hand",
        "expected_reduction_pct": 8,
        "difficulty": "medium",
        "estimated_cost": "Saves $1,000/year",
    },
    "remote_work": {
        "id": "scenario_remote",
        "name": "Work From Home",
        "description": "Eliminate daily commute by working remotely",
        "expected_reduction_pct": 20,
        "difficulty": "easy",
        "estimated_cost": "Saves $2,000/year",
    },
    "green_energy": {
        "id": "scenario_green_energy",
        "name": "100% Green Energy",
        "description": "Switch to 100% renewable energy provider",
        "expected_reduction_pct": 25,
        "difficulty": "easy",
        "estimated_cost": "+$20/month",
    },
    "sustainable_living": {
        "id": "scenario_sustainable",
        "name": "Sustainable Living Package",
        "description": "Combine plant-based diet, public transport, and renewable energy",
        "expected_reduction_pct": 45,
        "difficulty": "medium",
        "estimated_cost": "Saves $500/year",
    },
}

# Change impact factors
CHANGE_IMPACTS = {
    "replace_vehicle": {
        "car_petrol_to_ev": 0.69,       # 69% reduction in transport
        "car_petrol_to_hybrid": 0.46,
        "car_diesel_to_ev": 0.68,
    },
    "add_renewable": {
        "solar_panels": 0.60,            # 60% reduction in energy
        "green_provider": 0.80,          # 80% reduction
    },
    "change_diet": {
        "mixed_to_vegan": 0.40,          # 40% reduction in food
        "mixed_to_vegetarian": 0.32,
        "heavy_meat_to_mixed": 0.24,
    },
    "reduce_waste": {
        "full_recycling": 0.45,
        "composting": 0.15,
    },
    "reduce_shopping": {
        "second_hand_50": 0.30,
        "minimize": 0.50,
    },
}


class EcoTwinService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def simulate(
        self, user_id: UUID, data: SimulationRequest
    ) -> SimulationResponse:
        """Run an Eco Twin scenario simulation."""
        start_time = time.time()

        # Get latest footprint as baseline
        result = await self.db.execute(
            select(CarbonFootprint)
            .where(CarbonFootprint.user_id == user_id)
            .order_by(desc(CarbonFootprint.created_at))
            .limit(1)
        )
        baseline_fp = result.scalar_one_or_none()
        if not baseline_fp:
            raise NotFoundException("Carbon footprint", "No footprint calculated yet")

        baseline_monthly = float(baseline_fp.monthly_kg)
        baseline_annual = float(baseline_fp.annual_tons)
        breakdown = baseline_fp.breakdown or {}

        # Apply changes
        new_breakdown = copy.deepcopy(breakdown)
        total_upfront_cost = 0
        total_annual_savings = 0

        for change in data.changes:
            category = change.category
            if category in new_breakdown:
                impact = self._calculate_change_impact(change)
                reduction_factor = impact.get("reduction_factor", 0)
                new_breakdown[category] = round(
                    new_breakdown[category] * (1 - reduction_factor), 2
                )
                total_upfront_cost += impact.get("upfront_cost", 0)
                total_annual_savings += impact.get("annual_savings", 0)

        new_monthly = sum(new_breakdown.values())
        new_annual = round((new_monthly * 12) / 1000, 2)
        reduction_tons = round(baseline_annual - new_annual, 2)
        reduction_pct = round((reduction_tons / baseline_annual * 100) if baseline_annual > 0 else 0, 1)

        # Feasibility
        difficulty_score = min(100, sum(30 for c in data.changes if c.change_type in ("replace_vehicle", "add_renewable")))
        timeline_months = max(1, len(data.changes) * 2)

        calc_time = int((time.time() - start_time) * 1000)

        # Save simulation
        state = EcoTwinState(
            user_id=user_id,
            state_name="baseline",
            carbon_footprint_snapshot=breakdown,
            is_baseline=True,
        )
        self.db.add(state)
        await self.db.flush()

        simulation = EcoTwinSimulation(
            user_id=user_id,
            baseline_state_id=state.id,
            simulation_name=data.scenario_name,
            changes_applied=[c.model_dump() for c in data.changes],
            new_annual_tons=Decimal(str(new_annual)),
            reduction_tons=Decimal(str(reduction_tons)),
            reduction_percentage=Decimal(str(reduction_pct)),
            estimated_cost_annual=Decimal(str(total_upfront_cost)),
            savings_annual=Decimal(str(total_annual_savings)),
            difficulty_score=difficulty_score,
            ai_recommendation_score=max(20, 100 - difficulty_score),
            simulation_time_ms=calc_time,
        )
        self.db.add(simulation)
        await self.db.flush()

        return SimulationResponse(
            simulation_id=simulation.id,
            scenario_name=data.scenario_name,
            baseline={
                "annual_tons": baseline_annual,
                "monthly_kg": baseline_monthly,
            },
            simulated={
                "annual_tons": new_annual,
                "monthly_kg": round(new_monthly, 2),
            },
            impact={
                "reduction_tons": reduction_tons,
                "reduction_percentage": reduction_pct,
                "equivalent_trees": int(reduction_tons * 1000 / 21.77),
            },
            financial={
                "upfront_cost": total_upfront_cost,
                "annual_savings": total_annual_savings,
                "payback_period_years": round(total_upfront_cost / total_annual_savings, 1) if total_annual_savings > 0 else 0,
            },
            feasibility={
                "difficulty_score": difficulty_score,
                "timeline_months": timeline_months,
                "ai_recommendation_score": max(20, 100 - difficulty_score),
            },
            created_at=simulation.created_at,
        )

    def _calculate_change_impact(self, change) -> dict:
        """Calculate impact of a single change."""
        impacts = {
            "replace_vehicle": {"reduction_factor": 0.69, "upfront_cost": 45000, "annual_savings": 2400},
            "add_renewable": {"reduction_factor": 0.60, "upfront_cost": 15000, "annual_savings": 1200},
            "change_diet": {"reduction_factor": 0.40, "upfront_cost": 0, "annual_savings": 500},
            "reduce_waste": {"reduction_factor": 0.30, "upfront_cost": 100, "annual_savings": 200},
            "reduce_shopping": {"reduction_factor": 0.30, "upfront_cost": 0, "annual_savings": 1000},
            "use_public_transport": {"reduction_factor": 0.50, "upfront_cost": 0, "annual_savings": 3000},
        }
        return impacts.get(change.change_type, {"reduction_factor": 0.1, "upfront_cost": 0, "annual_savings": 0})

    async def get_simulations(self, user_id: UUID) -> list:
        result = await self.db.execute(
            select(EcoTwinSimulation)
            .where(EcoTwinSimulation.user_id == user_id)
            .order_by(desc(EcoTwinSimulation.created_at))
        )
        return result.scalars().all()

    @staticmethod
    def get_prebuilt_scenarios() -> list:
        return list(PREBUILT_SCENARIOS.values())
