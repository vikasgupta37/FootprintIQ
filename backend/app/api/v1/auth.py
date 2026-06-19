"""Auth API — register, login, OAuth, refresh, logout."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.schemas import (
    GoogleOAuthRequest,
    RefreshTokenRequest,
    TokenResponse,
    UserLogin,
    UserProfile,
    UserRegister,
)
from app.services.user_service import UserService

router = APIRouter()


@router.post("/register", response_model=dict, status_code=201)
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    user, tokens = await service.register(data)
    return {
        "user": UserProfile.model_validate(user).model_dump(),
        "tokens": tokens.model_dump(),
    }


@router.post("/login", response_model=dict)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    user, tokens = await service.login(data.email, data.password)
    return {
        "user": UserProfile.model_validate(user).model_dump(),
        "tokens": tokens.model_dump(),
    }


@router.post("/oauth/google", response_model=dict)
async def google_oauth(data: GoogleOAuthRequest, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    user, tokens = await service.google_oauth(data.code, data.redirect_uri)
    return {
        "user": UserProfile.model_validate(user).model_dump(),
        "tokens": tokens.model_dump(),
    }


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(data: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    return await service.refresh_tokens(data.refresh_token)


@router.post("/logout")
async def logout():
    return {"message": "Logged out successfully"}
