"""
Unit tests for security utilities — JWT tokens, password hashing, and token verification.
"""

import uuid
from datetime import timedelta

import pytest
from jose import jwt

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    create_token_pair,
    hash_password,
    verify_access_token,
    verify_password,
    verify_refresh_token,
)


# ── Password Hashing ────────────────────────────────────────────

class TestPasswordHashing:
    """Tests for bcrypt password hashing and verification."""

    def test_hash_password_returns_hash(self):
        """Hashed password should not match the plaintext."""
        hashed = hash_password("my_secure_p@ss")
        assert hashed != "my_secure_p@ss"
        assert hashed.startswith("$2")

    def test_verify_correct_password(self):
        """Correct password should verify successfully."""
        hashed = hash_password("correct_horse_battery_staple")
        assert verify_password("correct_horse_battery_staple", hashed) is True

    def test_verify_wrong_password(self):
        """Incorrect password should fail verification."""
        hashed = hash_password("correct_horse_battery_staple")
        assert verify_password("wrong_password", hashed) is False

    def test_different_hashes_for_same_password(self):
        """Two hashes of the same password should differ (salted)."""
        h1 = hash_password("same_password")
        h2 = hash_password("same_password")
        assert h1 != h2


# ── JWT Token Creation ───────────────────────────────────────────

class TestJWTCreation:
    """Tests for JWT token creation and structure."""

    def test_access_token_contains_subject(self):
        """Access token should contain the user ID as 'sub'."""
        user_id = str(uuid.uuid4())
        token = create_access_token(data={"sub": user_id, "email": "test@test.com", "role": "user"})
        payload = jwt.decode(token, settings.SECRET_KEY.get_secret_value(), algorithms=[settings.ALGORITHM])
        assert payload["sub"] == user_id

    def test_access_token_has_type(self):
        """Access token should have type='access'."""
        token = create_access_token(data={"sub": "123", "email": "test@test.com", "role": "user"})
        payload = jwt.decode(token, settings.SECRET_KEY.get_secret_value(), algorithms=[settings.ALGORITHM])
        assert payload["type"] == "access"

    def test_refresh_token_has_type(self):
        """Refresh token should have type='refresh'."""
        token = create_refresh_token(data={"sub": "123", "email": "test@test.com", "role": "user"})
        payload = jwt.decode(token, settings.SECRET_KEY.get_secret_value(), algorithms=[settings.ALGORITHM])
        assert payload["type"] == "refresh"

    def test_token_pair_returns_two_tokens(self):
        """Token pair should return both access and refresh tokens."""
        user_id = str(uuid.uuid4())
        access, refresh = create_token_pair(user_id, "test@test.com", "user")
        assert access is not None
        assert refresh is not None
        assert access != refresh

    def test_custom_expiry(self):
        """Token with custom expiry should respect the delta."""
        token = create_access_token(
            data={"sub": "123", "email": "t@t.com", "role": "user"},
            expires_delta=timedelta(minutes=5),
        )
        payload = jwt.decode(token, settings.SECRET_KEY.get_secret_value(), algorithms=[settings.ALGORITHM])
        assert "exp" in payload


# ── JWT Token Verification ───────────────────────────────────────

class TestJWTVerification:
    """Tests for JWT token verification logic."""

    def test_verify_valid_access_token(self):
        """Valid access token should verify successfully."""
        user_id = str(uuid.uuid4())
        token = create_access_token(data={"sub": user_id, "email": "t@t.com", "role": "user"})
        payload = verify_access_token(token)
        assert payload is not None
        assert payload["sub"] == user_id

    def test_verify_rejects_refresh_as_access(self):
        """Refresh token should be rejected when verified as access token."""
        token = create_refresh_token(data={"sub": "123", "email": "t@t.com", "role": "user"})
        result = verify_access_token(token)
        # Should return None or raise because type != "access"
        assert result is None

    def test_verify_valid_refresh_token(self):
        """Valid refresh token should verify successfully."""
        user_id = str(uuid.uuid4())
        token = create_refresh_token(data={"sub": user_id, "email": "t@t.com", "role": "user"})
        payload = verify_refresh_token(token)
        assert payload is not None
        assert payload["sub"] == user_id

    def test_verify_rejects_access_as_refresh(self):
        """Access token should be rejected when verified as refresh token."""
        token = create_access_token(data={"sub": "123", "email": "t@t.com", "role": "user"})
        result = verify_refresh_token(token)
        assert result is None

    def test_verify_rejects_expired_token(self):
        """Expired token should be rejected."""
        token = create_access_token(
            data={"sub": "123", "email": "t@t.com", "role": "user"},
            expires_delta=timedelta(seconds=-1),  # Already expired
        )
        result = verify_access_token(token)
        assert result is None

    def test_verify_rejects_tampered_token(self):
        """Token signed with a different key should be rejected."""
        payload = {"sub": "123", "email": "t@t.com", "role": "user", "type": "access", "exp": 9999999999}
        token = jwt.encode(payload, "wrong-secret-key", algorithm="HS256")
        result = verify_access_token(token)
        assert result is None

    def test_verify_rejects_garbage_input(self):
        """Completely invalid token string should be rejected."""
        result = verify_access_token("not.a.real.token")
        assert result is None
