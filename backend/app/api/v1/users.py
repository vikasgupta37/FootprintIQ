"""Users API — profile management."""

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.api.dependencies.services import get_user_service
from app.models.user import User
from app.schemas.schemas import UserProfile, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


@router.get("/me", response_model=UserProfile)
async def get_my_profile(user: User = Depends(get_current_user)):
    """Get current user's profile."""
    return UserProfile.model_validate(user)


@router.put("/me", response_model=UserProfile)
async def update_my_profile(
    data: UserUpdate,
    user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    """Update current user's profile details."""
    updated = await service.update_profile(user.id, data)
    return UserProfile.model_validate(updated)
