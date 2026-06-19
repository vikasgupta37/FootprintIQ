"""Eco Twin API — scenario simulation."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.schemas import SimulationRequest, SimulationResponse
from app.services.ecotwin_service import EcoTwinService

router = APIRouter()


@router.post("/simulate", response_model=SimulationResponse)
async def run_simulation(
    data: SimulationRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = EcoTwinService(db)
    return await service.simulate(user.id, data)


@router.get("/simulations")
async def get_simulations(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = EcoTwinService(db)
    sims = await service.get_simulations(user.id)
    return {"data": [{"id": str(s.id), "scenario_name": s.simulation_name, "reduction_percentage": float(s.reduction_percentage), "created_at": s.created_at.isoformat()} for s in sims]}


@router.get("/scenarios")
async def get_prebuilt_scenarios():
    return {"scenarios": EcoTwinService.get_prebuilt_scenarios()}
