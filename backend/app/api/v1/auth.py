from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, oauth2_scheme
from app.api.dependencies.services import get_user_service
from app.core.cache import cache
from app.core.security import verify_access_token
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
async def register(
    data: UserRegister,
    service: UserService = Depends(get_user_service),
):
    """Register a new user account."""
    user, tokens = await service.register(data)
    return {
        "user": UserProfile.model_validate(user).model_dump(),
        "tokens": tokens.model_dump(),
    }


@router.post("/login", response_model=dict)
async def login(
    data: UserLogin,
    service: UserService = Depends(get_user_service),
):
    """Log in an existing user."""
    user, tokens = await service.login(data.email, data.password)
    return {
        "user": UserProfile.model_validate(user).model_dump(),
        "tokens": tokens.model_dump(),
    }


@router.post("/oauth/google", response_model=dict)
async def google_oauth(
    data: GoogleOAuthRequest,
    service: UserService = Depends(get_user_service),
):
    """Authenticate via Google OAuth."""
    user, tokens = await service.google_oauth(data.code, data.redirect_uri)
    return {
        "user": UserProfile.model_validate(user).model_dump(),
        "tokens": tokens.model_dump(),
    }


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    data: RefreshTokenRequest,
    service: UserService = Depends(get_user_service),
):
    """Refresh authentication tokens."""
    return await service.refresh_tokens(data.refresh_token)


@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    """Log out user and invalidate current token."""
    if token:
        try:
            payload = verify_access_token(token)
            if payload:
                exp = payload.get("exp")
                if exp:
                    from datetime import datetime, timezone
                    now = datetime.now(timezone.utc).timestamp()
                    ttl = int(exp - now)
                    if ttl > 0:
                        await cache.set(f"blacklist:{token}", "1", ttl=ttl)
        except Exception:
            pass
    return {"message": "Logged out successfully"}
