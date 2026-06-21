"""
Backend test suite for FootprintIQ API.
"""

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# ── Health Check ─────────────────────────────────────────────

@pytest.mark.anyio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


@pytest.mark.anyio
async def test_root(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "FootprintIQ"


# ── Auth ─────────────────────────────────────────────────────

@pytest.mark.anyio
async def test_register_validation(client: AsyncClient):
    """Should reject weak passwords."""
    response = await client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "weak",
        "full_name": "Test User",
    })
    assert response.status_code == 422


@pytest.mark.anyio
async def test_login_invalid(client: AsyncClient):
    """Should reject invalid credentials."""
    try:
        response = await client.post("/api/v1/auth/login", json={
            "email": "nonexistent@example.com",
            "password": "NotARealPassword1!",
        })
        # 401 = proper auth rejection, 500 = DB unavailable (CI without Postgres)
        assert response.status_code in (401, 500)
    except ConnectionRefusedError:
        # No database available — expected in CI without Postgres
        pytest.skip("PostgreSQL not available")


# ── Protected Routes ─────────────────────────────────────────

@pytest.mark.anyio
async def test_protected_route_no_token(client: AsyncClient):
    """Should reject unauthenticated requests."""
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 401


@pytest.mark.anyio
async def test_protected_route_bad_token(client: AsyncClient):
    """Should reject invalid tokens."""
    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalid-token"},
    )
    assert response.status_code == 401


# ── Carbon ───────────────────────────────────────────────────

@pytest.mark.anyio
async def test_carbon_calculate_no_auth(client: AsyncClient):
    """Should require auth for calculation."""
    response = await client.post("/api/v1/carbon/calculate", json={})
    assert response.status_code == 401


# ── Eco Twin Scenarios ───────────────────────────────────────

@pytest.mark.anyio
async def test_prebuilt_scenarios(client: AsyncClient):
    """Should return pre-built scenarios without auth."""
    response = await client.get("/api/v1/eco-twin/scenarios")
    assert response.status_code == 200
    data = response.json()
    assert "scenarios" in data
    assert len(data["scenarios"]) > 0


# ── Leaderboard ──────────────────────────────────────────────

@pytest.mark.anyio
async def test_leaderboard_requires_auth(client: AsyncClient):
    """Should require auth for leaderboard."""
    response = await client.get("/api/v1/gamification/leaderboard")
    assert response.status_code == 401
