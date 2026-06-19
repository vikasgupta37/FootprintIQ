"""AI Chat API — conversational AI with streaming support."""

from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.schemas import (
    ChatMessageRequest,
    ChatMessageResponse,
    ConversationResponse,
    MessageResponse,
)
from app.services.ai_service import AIService

router = APIRouter()


@router.post("/chat", response_model=ChatMessageResponse)
async def send_message(
    data: ChatMessageRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = AIService(db)
    return await service.chat(user, data.message, data.conversation_id)


@router.post("/chat/stream")
async def stream_message(
    data: ChatMessageRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = AIService(db)
    return StreamingResponse(
        service.stream_chat(user, data.message, data.conversation_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/conversations", response_model=list[ConversationResponse])
async def get_conversations(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = AIService(db)
    convs = await service.get_conversations(user.id)
    return [ConversationResponse.model_validate(c) for c in convs]


@router.get("/conversations/{conversation_id}/messages", response_model=list[MessageResponse])
async def get_messages(
    conversation_id: UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = AIService(db)
    msgs = await service.get_messages(conversation_id, user.id)
    return [MessageResponse.model_validate(m) for m in msgs]
