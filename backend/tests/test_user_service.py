"""
Unit tests for UserService — registration, login, and profile management.
Tests use mocked DB sessions to verify service-level business logic.
"""

import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy import select

from app.core.exceptions import (
    AuthenticationException,
    ConflictException,
    NotFoundException,
)
from app.core.security import hash_password
from app.models.user import User
from app.schemas.schemas import UserRegister, UserUpdate
from app.services.user_service import UserService


class TestUserRegistration:
    """Tests for user registration logic in UserService."""

    @pytest.mark.asyncio
    async def test_register_success(self, mock_db):
        """Should successfully register a new user and return user info with tokens."""
        # Setup mock return for select query: no existing user
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result

        service = UserService(mock_db)
        data = UserRegister(
            email="newuser@example.com",
            password="SecurePassword123!",
            full_name="New User",
        )

        user, tokens = await service.register(data)

        # Assertions
        assert user.email == "newuser@example.com"
        assert user.full_name == "New User"
        assert user.password_hash is not None
        assert tokens.access_token is not None
        assert tokens.refresh_token is not None
        mock_db.add.assert_called_once()
        mock_db.flush.assert_called_once()

    @pytest.mark.asyncio
    async def test_register_existing_email_fails(self, mock_db):
        """Should raise ConflictException when registering an email that already exists."""
        # Setup mock return for select query: existing user found
        existing_user = User(email="existing@example.com")
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = existing_user
        mock_db.execute.return_value = mock_result

        service = UserService(mock_db)
        data = UserRegister(
            email="existing@example.com",
            password="SecurePassword123!",
            full_name="Existing User",
        )

        with pytest.raises(ConflictException) as excinfo:
            await service.register(data)

        assert "Email already registered" in str(excinfo.value)
        mock_db.add.assert_not_called()


class TestUserLogin:
    """Tests for user login logic in UserService."""

    @pytest.mark.asyncio
    async def test_login_success(self, mock_db):
        """Should successfully authenticate and return user info with tokens."""
        # Setup existing user with hashed password
        raw_password = "MySecurePassword123!"
        hashed = hash_password(raw_password)
        db_user = User(
            id=uuid.uuid4(),
            email="user@example.com",
            password_hash=hashed,
            is_active=True,
        )

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = db_user
        mock_db.execute.return_value = mock_result

        service = UserService(mock_db)
        user, tokens = await service.login("user@example.com", raw_password)

        assert user.email == "user@example.com"
        assert user.last_login is not None
        assert tokens.access_token is not None
        mock_db.flush.assert_called_once()

    @pytest.mark.asyncio
    async def test_login_invalid_password_fails(self, mock_db):
        """Should raise AuthenticationException for incorrect passwords."""
        db_user = User(
            email="user@example.com",
            password_hash=hash_password("correct_password"),
            is_active=True,
        )

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = db_user
        mock_db.execute.return_value = mock_result

        service = UserService(mock_db)

        with pytest.raises(AuthenticationException) as excinfo:
            await service.login("user@example.com", "wrong_password")

        assert "Invalid email or password" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_login_inactive_user_fails(self, mock_db):
        """Should raise AuthenticationException for inactive users."""
        db_user = User(
            email="user@example.com",
            password_hash=hash_password("password"),
            is_active=False,
        )

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = db_user
        mock_db.execute.return_value = mock_result

        service = UserService(mock_db)

        with pytest.raises(AuthenticationException) as excinfo:
            await service.login("user@example.com", "password")

        assert "Account is deactivated" in str(excinfo.value)


class TestUserProfileMethods:
    """Tests for profile retrieval and update logic in UserService."""

    @pytest.mark.asyncio
    async def test_get_profile_success(self, mock_db):
        """Should retrieve user profile if ID is valid."""
        user_id = uuid.uuid4()
        db_user = User(id=user_id, email="user@example.com")

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = db_user
        mock_db.execute.return_value = mock_result

        service = UserService(mock_db)
        profile = await service.get_profile(user_id)

        assert profile.id == user_id
        assert profile.email == "user@example.com"

    @pytest.mark.asyncio
    async def test_get_profile_not_found(self, mock_db):
        """Should raise NotFoundException if user ID does not exist."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result

        service = UserService(mock_db)
        user_id = uuid.uuid4()

        with pytest.raises(NotFoundException) as excinfo:
            await service.get_profile(user_id)

        assert "User" in str(excinfo.value)
        assert str(user_id) in str(excinfo.value)

    @pytest.mark.asyncio
    @patch("app.services.user_service.cache")
    async def test_update_profile_success(self, mock_cache, mock_db):
        """Should successfully update profile and invalidate cache."""
        user_id = uuid.uuid4()
        db_user = User(id=user_id, email="user@example.com", full_name="Old Name")

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = db_user
        mock_db.execute.return_value = mock_result

        mock_cache.delete = AsyncMock()
        mock_cache.user_profile_key.return_value = f"user:profile:{user_id}"

        service = UserService(mock_db)
        update_data = UserUpdate(full_name="New Name")
        updated_user = await service.update_profile(user_id, update_data)

        assert updated_user.full_name == "New Name"
        mock_db.flush.assert_called_once()
        mock_cache.delete.assert_called_once_with(f"user:profile:{user_id}")
