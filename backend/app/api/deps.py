"""
API dependency injection — database sessions, current user, role checks.
"""

from typing import Optional
from uuid import UUID

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.cache import cache
from app.core.config import settings
from app.core.database import get_db
from app.core.exceptions import (
    AuthenticationException,
    AuthorizationException,
    RateLimitException,
)
from app.core.security import verify_access_token
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    auto_error=False,
)


async def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Extract and validate current user from JWT token."""
    if not token:
        raise AuthenticationException("Not authenticated")

    payload = verify_access_token(token)
    if payload is None:
        raise AuthenticationException("Invalid or expired token")

    user_id = payload.get("sub")
    if not user_id:
        raise AuthenticationException("Invalid token payload")

    # Check cache first — skip DB query on hit
    cache_key = cache.user_profile_key(user_id)
    cached_user = await cache.get(cache_key)
    if cached_user and isinstance(cached_user, dict):
        # Still verify the user exists via DB for security, but
        # use a lightweight existence check
        result = await db.execute(select(User).where(User.id == UUID(user_id)))
        user = result.scalar_one_or_none()
    else:
        result = await db.execute(select(User).where(User.id == UUID(user_id)))
        user = result.scalar_one_or_none()
        if user and user.is_active:
            # Populate cache for subsequent requests
            await cache.set(
                cache_key,
                {"id": str(user.id), "email": user.email, "role": user.role},
                ttl=300,
            )

    if user is None or not user.is_active:
        raise AuthenticationException("User not found or inactive")

    return user


async def get_optional_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> Optional[User]:
    """Get current user if token provided, None otherwise."""
    if not token:
        return None
    try:
        return await get_current_user(token, db)
    except AuthenticationException:
        return None


def require_role(*roles: str):
    """Dependency factory for role-based access control."""

    async def role_checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise AuthorizationException(
                f"Role '{user.role}' not authorized. Required: {', '.join(roles)}"
            )
        return user

    return role_checker


# Role shortcuts
require_admin = require_role("admin")
require_premium = require_role("premium", "admin")
require_corporate = require_role("corporate_manager", "admin")


class RateLimiter:
    """Redis-based API rate limiter."""

    def __init__(self, limit: int, period: int = 3600, resource: str = "default"):
        self.limit = limit
        self.period = period
        self.resource = resource

    async def __call__(
        self,
        request: Request,
        user: Optional[User] = Depends(get_optional_user),
    ):
        try:
            # Try to check cache connection status
            _ = cache.client
        except Exception:
            # If Redis cache is not active/available (e.g. initial setup), bypass rate limiting
            return

        # Identify user
        if user:
            identity = str(user.id)
        else:
            identity = request.client.host if request.client else "unknown"

        key = cache.rate_limit_key(identity, self.resource)
        count = await cache.increment(key, self.period)

        if count > self.limit:
            ttl = await cache.get_ttl(key)
            raise RateLimitException(retry_after=max(1, ttl))

