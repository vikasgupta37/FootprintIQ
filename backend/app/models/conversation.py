"""
AI conversation and message models.
Matches DATABASE_SCHEMA.md conversations and messages tables.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.core.database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    title = Column(String(255), nullable=True)
    summary = Column(Text, nullable=True)

    # Conversation state
    status = Column(String(20), default="active")  # active, archived, deleted
    message_count = Column(Integer, default=0)

    # AI context
    context_data = Column(JSONB, default=dict)  # Stored context for AI continuation
    last_intent = Column(String(100), nullable=True)

    # Metadata
    total_tokens_used = Column(Integer, default=0)
    total_cost = Column(Integer, default=0)  # in microcents

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan", order_by="Message.created_at")


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)

    role = Column(String(20), nullable=False)  # user, assistant, system, tool
    content = Column(Text, nullable=False)

    # AI metadata
    intent = Column(String(100), nullable=True)
    agent_used = Column(String(50), nullable=True)  # orchestrator, advisor, carbon_engine, eco_twin
    tokens_used = Column(Integer, default=0)
    response_time_ms = Column(Integer, nullable=True)

    # Tool calls (JSONB array)
    tool_calls = Column(JSONB, default=list)

    # Feedback
    rating = Column(Integer, nullable=True)  # 1-5
    feedback = Column(Text, nullable=True)

    # Metadata
    metadata_ = Column("metadata", JSONB, default=dict)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
