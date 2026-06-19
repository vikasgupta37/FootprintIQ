"""Users API — profile management."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.schemas import UserProfile, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


@router.get("/me", response_model=UserProfile)
async def get_my_profile(user: User = Depends(get_current_user)):
    return UserProfile.model_validate(user)


@router.put("/me", response_model=UserProfile)
async def update_my_profile(
    data: UserUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = UserService(db)
    updated = await service.update_profile(user.id, data)
    return UserProfile.model_validate(updated)
