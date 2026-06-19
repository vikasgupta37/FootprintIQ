"""Carbon API — footprint calculation, history, trends."""

from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.schemas import (
    CarbonCalculateRequest,
    CarbonHistoryItem,
    CarbonScoreResponse,
    CarbonTrendsResponse,
)
from app.services.carbon_service import CarbonService

router = APIRouter()


@router.post("/calculate", response_model=CarbonScoreResponse, status_code=201)
async def calculate_footprint(
    data: CarbonCalculateRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CarbonService(db)
    return await service.calculate_footprint(user.id, data)


@router.get("/footprints", response_model=list[CarbonHistoryItem])
async def get_footprint_history(
    limit: int = 12,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CarbonService(db)
    footprints = await service.get_history(user.id, limit)
    return [CarbonHistoryItem.model_validate(fp) for fp in footprints]


@router.get("/footprints/{footprint_id}", response_model=CarbonScoreResponse)
async def get_footprint(
    footprint_id: UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CarbonService(db)
    fp = await service.get_footprint(footprint_id, user.id)
    return fp


@router.get("/trends")
async def get_trends(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = CarbonService(db)
    return await service.get_trends(user.id)
