"""
Recommendation model — AI-generated sustainability recommendations.
Matches DATABASE_SCHEMA.md recommendations and recommendation_actions tables.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.core.database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Content
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    detailed_steps = Column(JSONB, default=list)  # Step-by-step implementation
    visualization_data = Column(JSONB, default=dict)  # Data for charts (e.g. before/after)

    # Classification
    category = Column(String(50), nullable=False)  # transportation, energy, food, shopping, waste
    difficulty = Column(String(20), default="medium")  # easy, medium, hard
    priority_score = Column(Integer, default=50)  # 0-100

    # Impact Metrics
    estimated_co2_savings_kg = Column(Numeric(10, 2), default=0)
    estimated_cost_savings = Column(Numeric(10, 2), default=0)
    estimated_time_weeks = Column(Integer, default=4)
    impact_level = Column(String(20), default="medium")  # low, medium, high

    # Status
    status = Column(String(20), default="pending")  # pending, accepted, rejected, in_progress, completed
    is_active = Column(Boolean, default=True)

    # AI
    ai_model = Column(String(50), default="claude-opus-4.5")
    confidence_score = Column(Numeric(3, 2), default=0.85)
    reasoning = Column(Text, nullable=True)

    # Metadata
    source = Column(String(50), default="ai_generated")  # ai_generated, curated, community

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="recommendations")
    actions = relationship("RecommendationAction", back_populates="recommendation", cascade="all, delete-orphan")


class RecommendationAction(Base):
    __tablename__ = "recommendation_actions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recommendation_id = Column(UUID(as_uuid=True), ForeignKey("recommendations.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    action_type = Column(String(50), nullable=False)  # accepted, rejected, started, completed, paused
    notes = Column(Text, nullable=True)

    # Progress
    progress_percentage = Column(Integer, default=0)
    milestones_completed = Column(JSONB, default=list)

    # Actual impact
    actual_co2_saved_kg = Column(Numeric(10, 2), nullable=True)
    actual_cost_impact = Column(Numeric(10, 2), nullable=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    recommendation = relationship("Recommendation", back_populates="actions")
