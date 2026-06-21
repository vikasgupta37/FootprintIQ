"""
User model — core user entity for authentication and profile.
Matches DATABASE_SCHEMA.md users table specification.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)  # Null for OAuth users
    full_name = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, nullable=True, index=True)
    avatar_url = Column(Text, nullable=True)

    # Auth & Role
    role = Column(String(20), nullable=False, default="user")  # user, premium, admin, corporate_manager
    auth_provider = Column(String(20), nullable=False, default="email")  # email, google
    google_id = Column(String(255), unique=True, nullable=True)
    email_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    # Profile
    country = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    bio = Column(Text, nullable=True)
    household_size = Column(Integer, default=1)

    # Preferences (JSONB)
    preferences = Column(JSONB, default=dict)
    notification_preferences = Column(JSONB, default=lambda: {
        "email_weekly_summary": True,
        "email_recommendations": True,
        "push_achievements": True,
        "push_challenges": True,
    })

    # Gamification
    total_points = Column(Integer, default=0)
    level = Column(Integer, default=1)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    carbon_saved_kg = Column(Integer, default=0)

    # Organization (for corporate accounts)
    organization_id = Column(UUID(as_uuid=True), nullable=True)

    # Timestamps
    last_login = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    carbon_footprints = relationship("CarbonFootprint", back_populates="user", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="user", cascade="all, delete-orphan")
    achievements = relationship("UserAchievement", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
