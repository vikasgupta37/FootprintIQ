"""
Gamification models — badges, challenges, leaderboards, achievements.
Matches DATABASE_SCHEMA.md gamification tables.
"""

import uuid
from datetime import date, datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship

from app.core.database import Base


class Badge(Base):
    __tablename__ = "badges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    display_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    icon_url = Column(Text, nullable=True)

    # Classification
    category = Column(String(50), nullable=False)  # engagement, carbon_reduction, social, learning
    rarity = Column(String(20), default="common")  # common, uncommon, rare, epic, legendary

    # Criteria
    criteria = Column(JSONB, nullable=False, default=dict)
    points_awarded = Column(Integer, default=50)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class UserAchievement(Base):
    __tablename__ = "user_achievements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    badge_id = Column(UUID(as_uuid=True), ForeignKey("badges.id"), nullable=False, index=True)

    unlocked_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    progress = Column(Integer, default=100)  # percentage
    notified = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="achievements")
    badge = relationship("Badge")


class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    display_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)

    # Classification
    category = Column(String(50), nullable=False)  # transportation, energy, food, shopping, waste, general
    challenge_type = Column(String(20), default="weekly")  # daily, weekly, monthly, one_time
    difficulty = Column(String(20), default="medium")

    # Requirements
    requirements = Column(JSONB, nullable=False, default=dict)
    duration_days = Column(Integer, default=7)

    # Rewards
    points_reward = Column(Integer, default=100)
    badge_reward_id = Column(UUID(as_uuid=True), ForeignKey("badges.id"), nullable=True)

    # Scheduling
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    is_recurring = Column(Boolean, default=False)

    # Stats
    participant_count = Column(Integer, default=0)
    completion_rate = Column(Numeric(5, 2), default=0)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class UserChallenge(Base):
    __tablename__ = "user_challenges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    challenge_id = Column(UUID(as_uuid=True), ForeignKey("challenges.id"), nullable=False, index=True)

    # Status
    status = Column(String(20), default="active")  # active, completed, failed, abandoned
    progress = Column(JSONB, default=dict)
    progress_percentage = Column(Integer, default=0)

    # Dates
    started_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Rewards
    points_earned = Column(Integer, default=0)
    badge_earned = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    challenge = relationship("Challenge")


class Leaderboard(Base):
    __tablename__ = "leaderboards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    leaderboard_type = Column(String(50), nullable=False)  # global, country, friends, organization
    period = Column(String(20), nullable=False)  # daily, weekly, monthly, all_time

    rank = Column(Integer, nullable=False)
    score = Column(Numeric(10, 2), nullable=False)
    metric_type = Column(String(50), nullable=False)  # points, reduction_pct, co2_saved

    group_id = Column(String(100), nullable=True)

    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)

    total_participants = Column(Integer, nullable=True)
    percentile = Column(Numeric(5, 2), nullable=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
