"""Recommendations API."""

from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.api.dependencies.services import get_recommendation_service
from app.core.exceptions import NotFoundException
from app.models.recommendation import Recommendation, RecommendationAction
from app.models.user import User
from app.schemas.schemas import RecommendationActionRequest, RecommendationResponse
from app.services.recommendation_service import RecommendationService

router = APIRouter()


@router.get("/", response_model=list[RecommendationResponse])
async def get_recommendations(
    category: str = Query(None),
    status: str = Query("all"),
    user: User = Depends(get_current_user),
    service: RecommendationService = Depends(get_recommendation_service),
):
    """Get active recommendations for the current user."""
    recs = await service.get_user_recommendations(user.id, category=category, status=status)
    return [RecommendationResponse.model_validate(r) for r in recs]


@router.post("/{recommendation_id}/actions")
async def take_action(
    recommendation_id: UUID,
    data: RecommendationActionRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Take an action on a specific recommendation (e.g. mark accepted, completed)."""
    # Note: Logic directly in controller here, but we'll leave it as is for now 
    # since it's simple DB operations that don't involve the recommendation generation.
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
