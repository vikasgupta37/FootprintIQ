"""Recommendations API."""

from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.exceptions import NotFoundException
from app.models.recommendation import Recommendation, RecommendationAction
from app.models.user import User
from app.schemas.schemas import RecommendationActionRequest, RecommendationResponse

router = APIRouter()


@router.get("/", response_model=list[RecommendationResponse])
async def get_recommendations(
    category: str = Query(None),
    status: str = Query("all"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(Recommendation).where(Recommendation.user_id == user.id)
    if category:
        query = query.where(Recommendation.category == category)
    if status != "all":
        query = query.where(Recommendation.status == status)
    query = query.order_by(desc(Recommendation.priority_score)).limit(20)

    result = await db.execute(query)
    recs = result.scalars().all()
    return [RecommendationResponse.model_validate(r) for r in recs]


@router.post("/{recommendation_id}/actions")
async def take_action(
    recommendation_id: UUID,
    data: RecommendationActionRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Recommendation).where(
            Recommendation.id == recommendation_id,
            Recommendation.user_id == user.id,
        )
    )
    rec = result.scalar_one_or_none()
    if not rec:
        raise NotFoundException("Recommendation", str(recommendation_id))

    action = RecommendationAction(
        recommendation_id=recommendation_id,
        user_id=user.id,
        action_type=data.action_type,
        notes=data.notes,
        progress_percentage=data.progress_percentage or 0,
    )
    db.add(action)

    # Update recommendation status
    status_map = {
        "accepted": "accepted",
        "rejected": "rejected",
        "started": "in_progress",
        "completed": "completed",
        "paused": "accepted",
    }
    rec.status = status_map.get(data.action_type, rec.status)
    await db.flush()

    return {"status": "success", "action": data.action_type}
