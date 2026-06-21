import pytest
import uuid
import json
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.ai_service import AIService
from app.models.user import User
from app.models.conversation import Conversation, Message


@pytest.mark.anyio
@patch("app.services.ai_service.anthropic.AsyncAnthropic")
@patch("app.services.ai_service.settings")
@patch("app.core.database.AsyncSessionLocal")
async def test_stream_chat_success(mock_session_local, mock_settings, mock_anthropic_class):
    # Setup settings mock
    mock_settings.AI_MODEL = "claude-test-model"
    mock_settings.AI_MAX_TOKENS = 100
    mock_settings.AI_TEMPERATURE = 0.5
    mock_settings.ANTHROPIC_API_KEY = "mock-key"

    # Mock database session
    db_mock = AsyncMock()
    db_mock.add = MagicMock()
    db_mock.flush = AsyncMock()
    db_mock.commit = AsyncMock()
    
    # Mock SessionLocal factory to yield db_mock inside stream_chat
    mock_session = AsyncMock()
    mock_session.__aenter__.return_value = db_mock
    mock_session_local.return_value = mock_session
    
    # Mock user
    user = User(
        id=uuid.uuid4(),
        email="test@test.com",
        full_name="Test User",
        role="user",
        level=1,
        total_points=100
    )
    
    # Mock DB queries dynamically by statement contents
    mock_conv = Conversation(id=uuid.uuid4(), user_id=user.id, message_count=0)
    
    async def mock_execute(stmt, *args, **kwargs):
        stmt_str = str(stmt).lower()
        res = MagicMock()
        if "carbon_footprints" in stmt_str:
            res.scalar_one_or_none.return_value = None
        elif "conversations" in stmt_str:
            res.scalar_one_or_none.return_value = mock_conv
        elif "messages" in stmt_str:
            res.scalars().all.return_value = []
        else:
            res.scalar_one_or_none.return_value = None
            res.scalars().all.return_value = []
        return res
        
    db_mock.execute.side_effect = mock_execute
    
    # Mock Anthropic streaming client
    mock_client = AsyncMock()
    mock_anthropic_class.return_value = mock_client
    
    # Mock stream manager
    mock_stream = AsyncMock()
    
    # Simulate text event
    mock_event = MagicMock()
    mock_event.type = "text"
    mock_event.text = "Hello, I am your coach."
    
    # Make stream behave like an async iterator
    mock_stream.__aiter__.return_value = [mock_event].__iter__()
    
    # Mock get_final_message
    mock_final_message = MagicMock()
    mock_final_content = MagicMock()
    mock_final_content.type = "text"
    mock_final_content.text = "Hello, I am your coach."
    mock_final_message.content = [mock_final_content]
    mock_stream.get_final_message.return_value = mock_final_message
    
    # Mock client.messages.stream context manager
    mock_context_manager = MagicMock()
    mock_context_manager.__aenter__ = AsyncMock(return_value=mock_stream)
    mock_context_manager.__aexit__ = AsyncMock()
    mock_client.messages.stream = MagicMock(return_value=mock_context_manager)
    
    # Initialize service and run stream
    service = AIService(db_mock)
    
    generator = service.stream_chat(user, "hello coach")
    chunks = []
    async for chunk in generator:
        chunks.append(chunk)
        
    assert len(chunks) > 0
    # The first chunk should be the token chunk
    token_chunk = json.loads(chunks[0].replace("data: ", "").strip())
    assert token_chunk["type"] == "token"
    assert token_chunk["content"] == "Hello, I am your coach."
    
    # The last chunk should be the done chunk
    done_chunk = json.loads(chunks[-1].replace("data: ", "").strip())
    assert done_chunk["type"] == "done"
    
    # Assert DB methods were called
    db_mock.add.assert_called()
    db_mock.commit.assert_called_once()
