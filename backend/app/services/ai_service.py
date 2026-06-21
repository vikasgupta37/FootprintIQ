"""
AI Service — conversational agent and workflow orchestrator.
Refactored to use Clean Architecture and ToolRegistry.
"""

import json
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core.logging import logger
from app.core.llm import get_llm_client
from app.models.chat import Conversation, Message
from app.models.user import User
from app.schemas.schemas import ChatMessageResponse
from app.services.tools.registry import registry


class AIService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.client = get_llm_client()
        # System prompt defines the persona
        self.system_prompt = (
            "You are Claude, an expert AI Sustainability Advisor built by FootprintIQ. "
            "Your goal is to help users understand, track, and reduce their carbon footprint. "
            "Be encouraging, empathetic, and highly analytical. "
            "Always back up claims with data from your knowledge base. "
            "Use tools whenever the user asks to calculate their footprint, get recommendations, "
            "simulate a scenario (Eco Twin), or check their trends. "
            "Never give generic advice if you can use a tool to give personalized advice."
        )

    async def _get_or_create_conversation(self, user_id: UUID, conversation_id: UUID = None) -> Conversation:
        if conversation_id:
            res = await self.db.execute(
                select(Conversation)
                .options(joinedload(Conversation.messages))
                .where(Conversation.id == conversation_id, Conversation.user_id == user_id)
            )
            conv = res.unique().scalar_one_or_none()
            if not conv:
                raise HTTPException(status_code=404, detail="Conversation not found")
            return conv
            
        conv = Conversation(user_id=user_id, title="Sustainability Chat")
        self.db.add(conv)
        await self.db.commit()
        await self.db.refresh(conv)
        return conv

    async def get_conversations(self, user_id: UUID):
        """Get all conversations for a user."""
        res = await self.db.execute(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
        )
        return res.scalars().all()

    async def get_messages(self, conversation_id: UUID, user_id: UUID):
        """Get all messages in a conversation."""
        await self._get_or_create_conversation(user_id, conversation_id)
        res = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        )
        return res.scalars().all()

    async def chat(self, user: User, message_text: str, conversation_id: UUID = None) -> ChatMessageResponse:
        """Process a message and return the AI's response."""
        conv = await self._get_or_create_conversation(user.id, conversation_id)

        # Save user message
        user_msg = Message(
            conversation_id=conv.id,
            role="user",
            content=message_text
        )
        self.db.add(user_msg)
        await self.db.commit()

        # Get chat history
        history = await self.get_messages(conv.id, user.id)
        messages = [{"role": m.role, "content": m.content} for m in history]

        # Call Anthropic API with Tool Registry
        try:
            # 1. First call to Claude
            response = await self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                system=self.system_prompt,
                messages=messages,
                tools=registry.get_all_schemas(),
            )

            # 2. Process tools if any
            if response.stop_reason == "tool_use":
                assistant_message = {"role": "assistant", "content": response.content}
                messages.append(assistant_message)
                
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        tool_name = block.name
                        tool_args = block.input
                        tool_id = block.id

                        # Execute tool using registry
                        result_data = await registry.execute(tool_name, self.db, user, tool_args)
                        
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_id,
                            "content": json.dumps(result_data)
                        })
                
                messages.append({"role": "user", "content": tool_results})
                
                # 3. Second call with tool results
                final_response = await self.client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=1000,
                    system=self.system_prompt,
                    messages=messages,
                )
                ai_text = next(b.text for b in final_response.content if b.type == "text")
            else:
                ai_text = next(b.text for b in response.content if b.type == "text")

        except Exception as e:
            logger.error(f"LLM Error: {e}")
            ai_text = "I'm currently experiencing technical difficulties. Please try again later."

        # Save AI message
        ai_msg = Message(
            conversation_id=conv.id,
            role="assistant",
            content=ai_text
        )
        self.db.add(ai_msg)
        await self.db.commit()

        return ChatMessageResponse(
            id=ai_msg.id,
            conversation_id=conv.id,
            role=ai_msg.role,
            content=ai_msg.content,
            created_at=ai_msg.created_at
        )

    async def stream_chat(self, user: User, message_text: str, conversation_id: UUID = None):
        """Stream the AI's response."""
        # For simplicity in this refactor, we yield the full response
        # Real streaming with tools is complex and better handled sequentially or via SSE events
        res = await self.chat(user, message_text, conversation_id)
        yield f"data: {json.dumps({'content': res.content})}\n\n"
