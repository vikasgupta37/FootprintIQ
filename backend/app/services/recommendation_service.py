"""
Recommendation Service — AI-powered recommendation generation and management.
"""

import json

from typing import List, Optional
from uuid import UUID

import anthropic
from sqlalchemy import select, desc, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logging import logger
from app.models.carbon import CarbonFootprint
from app.models.recommendation import Recommendation
from app.models.user import User


RECOMMENDATION_PROMPT = """You are FootprintIQ's recommendation engine. Based on the user's carbon footprint data, generate 5 personalized, actionable sustainability recommendations.

## User Carbon Footprint
{footprint_data}

## Rules
1. Each recommendation must be specific and actionable
2. Include estimated CO₂ savings (in kg/month)
3. Include estimated cost savings (in USD/month)
4. Rate difficulty as easy/medium/hard
5. Rate impact as low/medium/high
6. Provide 3-5 concrete implementation steps

## Output Format (JSON array)
[
  {{
    "title": "Short actionable title",
    "description": "2-3 sentence description",
    "category": "transportation|energy|food|shopping|waste",
    "difficulty": "easy|medium|hard",
    "impact_level": "low|medium|high",
    "estimated_co2_savings_kg": 10.0,
    "estimated_cost_savings": 25.0,
    "estimated_time_weeks": 4,
    "priority_score": 85,
    "detailed_steps": [
      {{"step": 1, "title": "Step title", "description": "What to do"}}
    ],
    "visualization_data": {{
      "chart_type": "bar|doughnut|progress",
      "metric_label": "Transportation Emissions",
      "before_value": 100,
      "after_value": 78,
      "unit": "kg CO2"
    }},
    "reasoning": "Why this recommendation"
  }}
]"""


class RecommendationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def generate_recommendations(self, user_id: UUID) -> List[Recommendation]:
        """Generate AI-powered recommendations based on latest footprint."""
        # Get latest footprint
        result = await self.db.execute(
            select(CarbonFootprint)
            .where(CarbonFootprint.user_id == user_id)
            .order_by(desc(CarbonFootprint.created_at))
            .limit(1)
        )
        footprint = result.scalar_one_or_none()
        if not footprint:
            return []

        footprint_data = {
            "monthly_kg": float(footprint.monthly_kg),
            "annual_tons": float(footprint.annual_tons),
            "grade": footprint.grade,
            "breakdown": footprint.breakdown,
        }

        # Mark previous pending recommendations as inactive
        try:
            await self.db.execute(
                update(Recommendation)
                .where(
                    Recommendation.user_id == user_id,
                    Recommendation.status == "pending",
                    Recommendation.is_active == True,
                )
                .values(is_active=False)
            )
        except Exception as e:
            logger.warning(f"Failed to deactivate old pending recommendations: {e}")

        try:
            response = await self.client.messages.create(
                model=settings.AI_MODEL,
                max_tokens=2000,
                temperature=0.7,
                system="You are a sustainability expert. Output ONLY valid JSON.",
                messages=[{
                    "role": "user",
                    "content": RECOMMENDATION_PROMPT.format(
                        footprint_data=str(footprint_data)
                    ),
                }],
            )

            recs_data = json.loads(response.content[0].text)

            recommendations = []
            for rec_data in recs_data[:5]:
                rec = Recommendation(
                    user_id=user_id,
                    title=rec_data["title"],
                    description=rec_data["description"],
                    category=rec_data["category"],
                    difficulty=rec_data["difficulty"],
                    impact_level=rec_data["impact_level"],
                    estimated_co2_savings_kg=rec_data["estimated_co2_savings_kg"],
                    estimated_cost_savings=rec_data.get("estimated_cost_savings", 0),
                    estimated_time_weeks=rec_data.get("estimated_time_weeks", 4),
                    priority_score=rec_data.get("priority_score", 50),
                    detailed_steps=rec_data.get("detailed_steps", []),
                    visualization_data=rec_data.get("visualization_data", {}),
                    reasoning=rec_data.get("reasoning", ""),
                )
                self.db.add(rec)
                recommendations.append(rec)

            await self.db.flush()
            return recommendations

        except Exception as e:
            logger.error(f"Recommendation generation failed: {e}")
            return []

    async def get_user_recommendations(
        self,
        user_id: UUID,
        category: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 20,
    ) -> List[Recommendation]:
        """Get user's recommendations with optional filters."""
        query = select(Recommendation).where(
            Recommendation.user_id == user_id,
            Recommendation.is_active == True,
        )

        if category:
            query = query.where(Recommendation.category == category)
        if status and status != "all":
            query = query.where(Recommendation.status == status)

        query = query.order_by(desc(Recommendation.priority_score)).limit(limit)

        result = await self.db.execute(query)
        return result.scalars().all()
