"""
Shared test fixtures for FootprintIQ backend tests.
Provides mock database sessions, test users, token helpers,
and an async HTTP client for integration tests.
"""

import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.core.security import create_access_token, create_token_pair


# ── Constants ────────────────────────────────────────────────────

TEST_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")
TEST_USER_EMAIL = "test@footprintiq.com"
TEST_USER_PASSWORD = "SecureP@ss123"
TEST_USER_FULL_NAME = "Test User"


# ── User Factory ─────────────────────────────────────────────────

class FakeUser:
    """Lightweight user stub that matches the User model interface."""

    def __init__(
        self,
        id=TEST_USER_ID,
        email=TEST_USER_EMAIL,
        full_name=TEST_USER_FULL_NAME,
        role="user",
        is_active=True,
        total_points=150,
        level=2,
        current_streak=3,
        longest_streak=7,
        username=None,
        avatar_url=None,
    ):
        self.id = id
        self.email = email
        self.full_name = full_name
        self.role = role
        self.is_active = is_active
        self.total_points = total_points
        self.level = level
        self.current_streak = current_streak
        self.longest_streak = longest_streak
        self.username = username
        self.avatar_url = avatar_url
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)


def make_user(**overrides) -> FakeUser:
    """Factory helper — returns a FakeUser with optional overrides."""
    return FakeUser(**overrides)


# ── Token Helpers ────────────────────────────────────────────────

def make_access_token(
    user_id: uuid.UUID = TEST_USER_ID,
    email: str = TEST_USER_EMAIL,
    role: str = "user",
) -> str:
    """Generate a valid JWT access token for testing."""
    return create_access_token(
        data={"sub": str(user_id), "email": email, "role": role}
    )


def auth_header(
    user_id: uuid.UUID = TEST_USER_ID,
    email: str = TEST_USER_EMAIL,
    role: str = "user",
) -> dict:
    """Return an Authorization header dict for test requests."""
    token = make_access_token(user_id, email, role)
    return {"Authorization": f"Bearer {token}"}


# ── Mock DB Session ──────────────────────────────────────────────

@pytest.fixture
def mock_db():
    """Create a mock async database session."""
    session = AsyncMock()
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.flush = AsyncMock()
    session.refresh = AsyncMock()
    session.add = MagicMock()
    session.rollback = AsyncMock()
    return session


# ── Async Client ─────────────────────────────────────────────────

@pytest_asyncio.fixture
async def client() -> AsyncGenerator:
    """Provide an async HTTP test client against the FastAPI app."""
    from app.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
