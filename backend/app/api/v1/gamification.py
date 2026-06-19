"""Gamification API — points, badges, challenges, leaderboard."""

from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.schemas import PointsResponse
from app.services.gamification_service import GamificationService

router = APIRouter()


@router.get("/points", response_model=PointsResponse)
async def get_points(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = GamificationService(db)
    return await service.get_points(user)


@router.get("/badges")
async def get_badges(
    status: str = Query("all"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = GamificationService(db)
    return {"badges": await service.get_badges(user.id, status)}


@router.get("/challenges")
async def get_challenges(
    status: str = Query("available"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = GamificationService(db)
    return {"challenges": await service.get_challenges(user.id, status)}


@router.post("/challenges/{challenge_id}/join")
async def join_challenge(
    challenge_id: UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = GamificationService(db)
    return await service.join_challenge(user.id, challenge_id)


@router.get("/leaderboard")
async def get_leaderboard(
    type: str = Query("global"),
    period: str = Query("weekly"),
    metric: str = Query("points"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = GamificationService(db)
    return await service.get_leaderboard(type, period, metric)
