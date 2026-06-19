"""
Carbon Service — carbon footprint calculation engine with emission factors.
Implements IPCC-validated emission factors and grade assignment.
"""

import time
from decimal import Decimal
from typing import Dict, List, Optional, Tuple
from uuid import UUID

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.cache import cache
from app.core.exceptions import NotFoundException
from app.models.carbon import CarbonCategory, CarbonFootprint
from app.schemas.schemas import (
    CarbonCalculateRequest,
    CarbonScoreResponse,
    CategoryBreakdown,
)


# ── Emission Factors (kg CO2e) ───────────────────────────────────
# Source: IPCC AR6, EPA, Carbon Footprint Ltd.

VEHICLE_EMISSION_FACTORS = {
    "car_petrol": 0.171,       # kg CO2e per km
    "car_diesel": 0.168,
    "car_hybrid": 0.092,
    "ev": 0.053,
    "motorcycle": 0.103,
    "none": 0.0,
}

PUBLIC_TRANSPORT_FACTOR = 0.089  # kg CO2e per km (average bus/metro)

FLIGHT_EMISSIONS = {
    "short_haul": 255,   # kg CO2e per flight (avg domestic round-trip)
    "long_haul": 1240,   # kg CO2e per flight (avg international round-trip)
}

ELECTRICITY_FACTOR = 0.309  # kg CO2e per kWh (US average grid)

HEATING_FACTORS = {
    "electric": 0.309,
    "gas": 0.184,
    "oil": 0.245,
    "heat_pump": 0.100,
}

DIET_FACTORS = {
    "vegan": 1.5,           # tons CO2e per year
    "vegetarian": 1.7,
    "pescatarian": 1.9,
    "mixed": 2.5,
    "heavy_meat": 3.3,
}

DAIRY_MULTIPLIERS = {
    "none": 0.0,
    "low": 0.8,
    "moderate": 1.0,
    "high": 1.3,
}

# Average kg CO2e per item
SHOPPING_FACTORS = {
    "clothing_item": 25.0,
    "electronics_item": 200.0,
    "online_delivery": 3.5,
}

RECYCLING_REDUCTION = {
    "never": 0.0,
    "sometimes": 0.15,
    "often": 0.30,
    "always": 0.45,
}

# Grade thresholds (monthly kg CO2e)
GRADE_THRESHOLDS = [
    (200,  "EXCELLENT", "#10B981"),  # green
    (350,  "GOOD",      "#34D399"),
    (500,  "MODERATE",  "#FBBF24"),  # amber
    (700,  "HIGH",      "#F97316"),  # orange
    (9999, "CRITICAL",  "#EF4444"),  # red
]

# Comparisons (monthly kg)
COMPARISON_AVERAGES = {
    "us_average": 1370,    # ~16.4 tons/year
    "eu_average": 567,     # ~6.8 tons/year
    "global_average": 400, # ~4.8 tons/year
    "target_2c": 183,      # ~2.2 tons/year (Paris Agreement)
    "india_average": 158,  # ~1.9 tons/year
}


class CarbonService:
    def __init__(self, db: Optional[AsyncSession] = None):
        self.db = db

    async def calculate_footprint(
        self, user_id: UUID, data: CarbonCalculateRequest
    ) -> CarbonScoreResponse:
        """Calculate complete carbon footprint from user inputs."""
        start_time = time.time()

        # Calculate each category
        transport_kg = self._calculate_transportation(data.transportation)
        energy_kg = self._calculate_energy(data.energy)
        food_kg = self._calculate_food(data.food)
        shopping_kg = self._calculate_shopping(data.shopping)
        waste_kg = self._calculate_waste(data.waste)

        total_monthly = transport_kg + energy_kg + food_kg + shopping_kg + waste_kg
        annual_tons = round((total_monthly * 12) / 1000, 2)
        daily_kg = round(total_monthly / 30, 2)

        # Grade
        grade, grade_color = self._assign_grade(total_monthly)

        # Breakdown
        categories = [
            ("transportation", transport_kg),
            ("energy", energy_kg),
            ("food", food_kg),
            ("shopping", shopping_kg),
            ("waste", waste_kg),
        ]
        breakdown_list = []
        for cat_name, cat_kg in categories:
            pct = round((cat_kg / total_monthly * 100) if total_monthly > 0 else 0, 1)
            breakdown_list.append(CategoryBreakdown(
                category=cat_name,
                monthly_kg=round(cat_kg, 2),
                percentage=pct,
            ))

        # Generate insights
        insights = self._generate_insights(categories, total_monthly, grade)

        calc_time = int((time.time() - start_time) * 1000)

        # Save to database
        footprint = CarbonFootprint(
            user_id=user_id,
            monthly_kg=Decimal(str(round(total_monthly, 2))),
            annual_tons=Decimal(str(annual_tons)),
            daily_kg=Decimal(str(daily_kg)),
            grade=grade,
            grade_color=grade_color,
            breakdown={cat: round(kg, 2) for cat, kg in categories},
            input_data=data.model_dump(),
            country_average_kg=COMPARISON_AVERAGES["global_average"],
            global_average_kg=COMPARISON_AVERAGES["global_average"],
            target_2c_kg=COMPARISON_AVERAGES["target_2c"],
            insights=insights,
            calculation_time_ms=calc_time,
        )
        self.db.add(footprint)

        # Save category details
        for cat_name, cat_kg in categories:
            pct = round((cat_kg / total_monthly * 100) if total_monthly > 0 else 0, 1)
            cat = CarbonCategory(
                footprint_id=footprint.id,
                category=cat_name,
                monthly_kg=Decimal(str(round(cat_kg, 2))),
                percentage_of_total=Decimal(str(pct)),
            )
            self.db.add(cat)

        await self.db.flush()

        # Update cache
        await cache.set(
            cache.user_carbon_key(str(user_id)),
            {"monthly_kg": round(total_monthly, 2), "grade": grade},
            ttl=300,
        )

        return CarbonScoreResponse(
            id=footprint.id,
            monthly_kg=round(total_monthly, 2),
            annual_tons=annual_tons,
            daily_kg=daily_kg,
            grade=grade,
            grade_color=grade_color,
            breakdown=breakdown_list,
            comparisons=COMPARISON_AVERAGES,
            insights=insights,
            created_at=footprint.created_at,
        )

    # ── Calculation Methods ──────────────────────────────────────

    def _calculate_transportation(self, t) -> float:
        vehicle = VEHICLE_EMISSION_FACTORS.get(t.vehicle_type, 0.171) * t.km_per_month
        public = PUBLIC_TRANSPORT_FACTOR * t.public_transport_km
        flights = (
            t.flights_short_haul * FLIGHT_EMISSIONS["short_haul"]
            + t.flights_long_haul * FLIGHT_EMISSIONS["long_haul"]
        ) / 12  # annualize to monthly
        return vehicle + public + flights

    def _calculate_energy(self, e) -> float:
        electricity = e.electricity_kwh_per_month * ELECTRICITY_FACTOR
        renewable_reduction = electricity * (e.renewable_percentage / 100)
        heating = HEATING_FACTORS.get(e.heating_type, 0.309) * 500 / 12  # avg monthly
        ac = e.ac_usage_hours * 1.5 * 0.309 * 30 / 12  # per month estimate
        return (electricity - renewable_reduction) + heating + ac

    def _calculate_food(self, f) -> float:
        base = DIET_FACTORS.get(f.diet_type, 2.5) * 1000 / 12  # monthly kg
        dairy_mult = DAIRY_MULTIPLIERS.get(f.dairy_consumption, 1.0)
        waste_addition = base * (f.food_waste_pct / 100)
        local_reduction = base * (f.local_produce_pct / 100) * 0.1
        return (base * dairy_mult) + waste_addition - local_reduction

    def _calculate_shopping(self, s) -> float:
        clothing = s.clothing_items_per_month * SHOPPING_FACTORS["clothing_item"]
        electronics = s.electronics_per_year * SHOPPING_FACTORS["electronics_item"] / 12
        deliveries = s.online_deliveries_per_month * SHOPPING_FACTORS["online_delivery"]
        second_hand_reduction = (clothing + electronics) * (s.second_hand_pct / 100) * 0.6
        return clothing + electronics + deliveries - second_hand_reduction

    def _calculate_waste(self, w) -> float:
        base_waste = 50  # kg CO2e per month average
        recycling_red = RECYCLING_REDUCTION.get(w.recycling_frequency, 0)
        composting_red = 0.15 if w.composting else 0
        plastic_factor = {"low": 0.7, "moderate": 1.0, "high": 1.4}.get(w.plastic_usage, 1.0)
        bottle_red = 0.05 if w.reusable_water_bottle else 0
        return base_waste * plastic_factor * (1 - recycling_red - composting_red - bottle_red)

    def _assign_grade(self, monthly_kg: float) -> Tuple[str, str]:
        for threshold, grade, color in GRADE_THRESHOLDS:
            if monthly_kg <= threshold:
                return grade, color
        return "CRITICAL", "#EF4444"

    def _generate_insights(
        self, categories: list, total: float, grade: str
    ) -> List[str]:
        insights = []
        sorted_cats = sorted(categories, key=lambda x: x[1], reverse=True)
        top_cat, top_kg = sorted_cats[0]
        pct = round(top_kg / total * 100) if total > 0 else 0

        insights.append(
            f"Your largest category is {top_cat} at {pct}% of your total footprint."
        )

        if total < COMPARISON_AVERAGES["global_average"]:
            insights.append("You're below the global average — great job!")
        else:
            diff = round(total - COMPARISON_AVERAGES["global_average"], 1)
            insights.append(
                f"You're {diff} kg/month above the global average. "
                f"Focus on {top_cat} for the biggest impact."
            )

        if grade in ("HIGH", "CRITICAL"):
            insights.append(
                f"Your grade is {grade}. Small changes in {top_cat} can make a big difference."
            )

        return insights

    # ── History & Trends ─────────────────────────────────────────

    async def get_history(self, user_id: UUID, limit: int = 12) -> list:
        result = await self.db.execute(
            select(CarbonFootprint)
            .where(CarbonFootprint.user_id == user_id)
            .order_by(desc(CarbonFootprint.created_at))
            .limit(limit)
        )
        return result.scalars().all()

    async def get_footprint(self, footprint_id: UUID, user_id: UUID) -> CarbonFootprint:
        result = await self.db.execute(
            select(CarbonFootprint).where(
                CarbonFootprint.id == footprint_id,
                CarbonFootprint.user_id == user_id,
            )
        )
        fp = result.scalar_one_or_none()
        if not fp:
            raise NotFoundException("Carbon footprint", str(footprint_id))
        return fp

    async def get_trends(self, user_id: UUID) -> dict:
        history = await self.get_history(user_id, limit=12)
        if len(history) < 2:
            current = float(history[0].monthly_kg) if history else 0
            return {
                "current_month": current,
                "previous_month": 0,
                "change_pct": 0,
                "trend": "stable",
                "history": history,
            }

        current = float(history[0].monthly_kg)
        previous = float(history[1].monthly_kg)
        change_pct = round(((current - previous) / previous) * 100, 2) if previous else 0
        trend = "improving" if change_pct < -1 else ("worsening" if change_pct > 1 else "stable")

        return {
            "current_month": current,
            "previous_month": previous,
            "change_pct": change_pct,
            "trend": trend,
            "history": history,
        }
