"""
LLM Configuration and Provider.
Wraps the Anthropic client to ensure single instantiation and consistent configuration.
"""

import anthropic
from app.core.config import settings
from app.core.logging import logger

class LLMProvider:
    """Provides a configured instance of the Anthropic client."""
    
    _client = None

    @classmethod
    def get_client(cls) -> anthropic.AsyncAnthropic:
        """Get or initialize the AsyncAnthropic client."""
        if cls._client is None:
            if not settings.ANTHROPIC_API_KEY:
                logger.warning("ANTHROPIC_API_KEY is not set. LLM features may fail.")
            cls._client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        return cls._client

# Dependency injector
def get_llm_client() -> anthropic.AsyncAnthropic:
    return LLMProvider.get_client()
