"""
User Service — handles user CRUD, profile management, and Google OAuth.
"""

from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

import httpx
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.cache import cache
from app.core.config import settings
from app.core.exceptions import (
    AuthenticationException,
    ConflictException,
    NotFoundException,
)
from app.core.security import (
    create_token_pair,
    hash_password,
    verify_password,
    verify_refresh_token,
)
from app.models.user import User
from app.schemas.schemas import (
    TokenResponse,
    UserProfile,
    UserRegister,
    UserUpdate,
)


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ── Registration ─────────────────────────────────────────────

    async def register(self, data: UserRegister) -> tuple[User, TokenResponse]:
        """Register a new user with email/password."""
        # Check for existing user
        existing = await self.db.execute(
            select(User).where(User.email == data.email)
        )
        if existing.scalar_one_or_none():
            raise ConflictException("Email already registered")

        user = User(
            email=data.email,
            password_hash=hash_password(data.password),
            full_name=data.full_name,
            auth_provider="email",
            email_verified=False,
        )
        self.db.add(user)
        await self.db.flush()

        access, refresh = create_token_pair(str(user.id), user.email, user.role)
        token_response = TokenResponse(
            access_token=access,
            refresh_token=refresh,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        return user, token_response

    # ── Login ────────────────────────────────────────────────────

    async def login(self, email: str, password: str) -> tuple[User, TokenResponse]:
        """Authenticate user with email/password."""
        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if not user or not user.password_hash:
            raise AuthenticationException("Invalid email or password")
        if not verify_password(password, user.password_hash):
            raise AuthenticationException("Invalid email or password")
        if not user.is_active:
            raise AuthenticationException("Account is deactivated")

        # Update last login
        user.last_login = datetime.now(timezone.utc)
        await self.db.flush()

        access, refresh = create_token_pair(str(user.id), user.email, user.role)
        return user, TokenResponse(
            access_token=access,
            refresh_token=refresh,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    # ── Google OAuth ─────────────────────────────────────────────

    async def google_oauth(self, code: str, redirect_uri: Optional[str] = None) -> tuple[User, TokenResponse]:
        """Authenticate or register via Google OAuth."""
        # Exchange code for tokens
        async with httpx.AsyncClient() as client:
            token_resp = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "code": code,
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "redirect_uri": redirect_uri or settings.GOOGLE_REDIRECT_URI,
                    "grant_type": "authorization_code",
                },
            )
            if token_resp.status_code != 200:
                raise AuthenticationException("Failed to exchange OAuth code")
            tokens = token_resp.json()

            # Get user info
            userinfo_resp = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f'Bearer {tokens["access_token"]}'},
            )
            if userinfo_resp.status_code != 200:
                raise AuthenticationException("Failed to get user info from Google")
            google_user = userinfo_resp.json()

        google_id = google_user["id"]
        email = google_user["email"]
        name = google_user.get("name", email.split("@")[0])
        avatar = google_user.get("picture")

        # Check for existing user
        result = await self.db.execute(
            select(User).where(
                (User.google_id == google_id) | (User.email == email)
            )
        )
        user = result.scalar_one_or_none()

        if user:
            # Update Google info
            user.google_id = google_id
            user.avatar_url = avatar or user.avatar_url
            user.last_login = datetime.now(timezone.utc)
            user.email_verified = True
        else:
            # Create new user
            user = User(
                email=email,
                full_name=name,
                google_id=google_id,
                avatar_url=avatar,
                auth_provider="google",
                email_verified=True,
            )
            self.db.add(user)

        await self.db.flush()

        access, refresh = create_token_pair(str(user.id), user.email, user.role)
        return user, TokenResponse(
            access_token=access,
            refresh_token=refresh,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    # ── Token Refresh ────────────────────────────────────────────

    async def refresh_tokens(self, refresh_token: str) -> TokenResponse:
        """Generate new token pair from a valid refresh token."""
        payload = verify_refresh_token(refresh_token)
        if not payload:
            raise AuthenticationException("Invalid refresh token")

        user_id = payload.get("sub")
        result = await self.db.execute(select(User).where(User.id == UUID(user_id)))
        user = result.scalar_one_or_none()
        if not user or not user.is_active:
            raise AuthenticationException("User not found or inactive")

        access, refresh = create_token_pair(str(user.id), user.email, user.role)
        return TokenResponse(
            access_token=access,
            refresh_token=refresh,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    # ── Profile ──────────────────────────────────────────────────

    async def get_profile(self, user_id: UUID) -> User:
        """Get user by ID."""
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundException("User", str(user_id))
        return user

    async def update_profile(self, user_id: UUID, data: UserUpdate) -> User:
        """Update user profile fields."""
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundException("User", str(user_id))

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        user.updated_at = datetime.now(timezone.utc)
        await self.db.flush()

        # Invalidate cache
        await cache.delete(cache.user_profile_key(str(user_id)))

        return user
