"""
Eco Twin, Learning Content, Analytics, and Audit Log models.
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


# ── Eco Twin ─────────────────────────────────────────────────────

class EcoTwinState(Base):
    __tablename__ = "eco_twin_states"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    state_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    carbon_footprint_snapshot = Column(JSONB, nullable=False)
    transportation_model = Column(JSONB, default=dict)
    energy_model = Column(JSONB, default=dict)
    food_model = Column(JSONB, default=dict)
    shopping_model = Column(JSONB, default=dict)
    waste_model = Column(JSONB, default=dict)

    projected_annual_tons = Column(Numeric(10, 2), nullable=True)
    projected_30d_kg = Column(Numeric(10, 2), nullable=True)
    projected_90d_kg = Column(Numeric(10, 2), nullable=True)
    projected_365d_kg = Column(Numeric(10, 2), nullable=True)

    is_baseline = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))


class EcoTwinSimulation(Base):
    __tablename__ = "eco_twin_simulations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    baseline_state_id = Column(UUID(as_uuid=True), ForeignKey("eco_twin_states.id"), nullable=False)

    simulation_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    changes_applied = Column(JSONB, nullable=False)

    new_annual_tons = Column(Numeric(10, 2), nullable=False)
    reduction_tons = Column(Numeric(10, 2), nullable=False)
    reduction_percentage = Column(Numeric(5, 2), nullable=False)

    estimated_cost_annual = Column(Numeric(10, 2), nullable=True)
    savings_annual = Column(Numeric(10, 2), nullable=True)
    payback_period_months = Column(Integer, nullable=True)

    difficulty_score = Column(Integer, nullable=True)
    ai_recommendation_score = Column(Integer, nullable=True)

    ai_model = Column(String(50), default="claude-opus-4.5")
    simulation_time_ms = Column(Integer, nullable=True)

    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))


# ── Learning Content ─────────────────────────────────────────────

class LearningContent(Base):
    __tablename__ = "learning_content"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=False)

    category = Column(String(50), nullable=False)
    difficulty = Column(String(20), default="beginner")
    content_type = Column(String(50), nullable=False)  # article, video, infographic, quiz

    thumbnail_url = Column(Text, nullable=True)
    video_url = Column(Text, nullable=True)
    estimated_read_time = Column(Integer, nullable=True)

    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)

    meta_title = Column(String(255), nullable=True)
    meta_description = Column(Text, nullable=True)
    tags = Column(ARRAY(String), default=list)

    is_published = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    published_at = Column(DateTime(timezone=True), nullable=True)

    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=False)
    difficulty = Column(String(20), default="beginner")
    questions = Column(JSONB, nullable=False)
    total_points = Column(Integer, default=0)
    passing_score = Column(Integer, nullable=True)
    points_reward = Column(Integer, default=0)
    attempt_count = Column(Integer, default=0)
    average_score = Column(Numeric(5, 2), nullable=True)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"), nullable=False, index=True)
    score = Column(Integer, nullable=False)
    total_possible = Column(Integer, nullable=False)
    percentage = Column(Numeric(5, 2), nullable=True)
    passed = Column(Boolean, nullable=True)
    answers = Column(JSONB, nullable=False)
    time_taken_seconds = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))


# ── Analytics ────────────────────────────────────────────────────

class UserAnalytics(Base):
    __tablename__ = "user_analytics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    period_type = Column(String(20), nullable=False)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)

    login_count = Column(Integer, default=0)
    session_duration_minutes = Column(Integer, default=0)
    pages_viewed = Column(Integer, default=0)
    calculations_performed = Column(Integer, default=0)
    average_carbon_footprint = Column(Numeric(10, 2), nullable=True)
    carbon_reduction_pct = Column(Numeric(5, 2), nullable=True)
    ai_conversations = Column(Integer, default=0)
    ai_messages_sent = Column(Integer, default=0)
    points_earned = Column(Integer, default=0)
    badges_unlocked = Column(Integer, default=0)
    challenges_completed = Column(Integer, default=0)
    articles_read = Column(Integer, default=0)
    quizzes_taken = Column(Integer, default=0)
    recommendations_received = Column(Integer, default=0)
    recommendations_accepted = Column(Integer, default=0)
    recommendations_completed = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))


class SustainabilityReport(Base):
    __tablename__ = "sustainability_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    report_type = Column(String(20), default="weekly") # weekly, monthly
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    
    # Generated content from AI
    summary_text = Column(Text, nullable=False)
    key_insights = Column(JSONB, default=list) # e.g. [{"text": "...", "metric": "..."}]
    
    carbon_saved_kg = Column(Numeric(10, 2), nullable=True)
    points_earned = Column(Integer, default=0)
    challenges_completed = Column(Integer, default=0)
    
    ai_sustainability_score = Column(Integer, nullable=True) # 0-100
    
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

# ── Audit Logs ───────────────────────────────────────────────────

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    actor_type = Column(String(50), nullable=False)  # user, admin, system
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(UUID(as_uuid=True), nullable=True)
    description = Column(Text, nullable=True)
    changes = Column(JSONB, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    status = Column(String(20), default="success")
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
