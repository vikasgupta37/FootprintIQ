"""
Carbon footprint models — footprints, categories, and trends.
Matches DATABASE_SCHEMA.md carbon_footprints and carbon_categories tables.
"""

import uuid
from datetime import datetime, timezone
from decimal import Decimal

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


class CarbonFootprint(Base):
    __tablename__ = "carbon_footprints"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Carbon Scores
    monthly_kg = Column(Numeric(10, 2), nullable=False)
    annual_tons = Column(Numeric(10, 2), nullable=False)
    daily_kg = Column(Numeric(10, 2), nullable=True)

    # Grade: EXCELLENT, GOOD, MODERATE, HIGH, CRITICAL
    grade = Column(String(20), nullable=False)
    grade_color = Column(String(7), nullable=True)  # hex color
    
    # AI Score: 0-100
    ai_sustainability_score = Column(Integer, nullable=True)

    # Category Breakdown (JSONB)
    breakdown = Column(JSONB, nullable=False, default=dict)
    # Example: {"transportation": 162.5, "energy": 95.0, "food": 75.0, "shopping": 35.0, "waste": 19.5}

    # Input Data (raw inputs preserved)
    input_data = Column(JSONB, nullable=False, default=dict)

    # Comparisons
    country_average_kg = Column(Numeric(10, 2), nullable=True)
    global_average_kg = Column(Numeric(10, 2), nullable=True)
    target_2c_kg = Column(Numeric(10, 2), nullable=True)

    # AI-generated insights (JSONB array)
    insights = Column(JSONB, default=list)

    # Metadata
    calculation_method = Column(String(50), default="standard_v1")
    ai_model = Column(String(50), default="claude-opus-4.5")
    calculation_time_ms = Column(Integer, nullable=True)
    is_complete = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="carbon_footprints")
    categories = relationship("CarbonCategory", back_populates="footprint", cascade="all, delete-orphan")


class CarbonCategory(Base):
    __tablename__ = "carbon_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    footprint_id = Column(UUID(as_uuid=True), ForeignKey("carbon_footprints.id", ondelete="CASCADE"), nullable=False, index=True)

    # Category
    category = Column(String(50), nullable=False)  # transportation, energy, food, shopping, waste
    monthly_kg = Column(Numeric(10, 2), nullable=False)
    percentage_of_total = Column(Numeric(5, 2), nullable=True)

    # Detailed breakdown (JSONB)
    details = Column(JSONB, default=dict)
    # e.g. for transportation: {"car": 140.0, "public_transport": 15.5, "flights": 7.0}

    # Sub-category inputs
    input_data = Column(JSONB, default=dict)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    footprint = relationship("CarbonFootprint", back_populates="categories")
