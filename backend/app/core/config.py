"""
Application configuration using Pydantic Settings.
All environment variables are loaded from .env file.
"""

from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr, model_validator


class Settings(BaseSettings):
    # ── Application ──────────────────────────────────────────────
    PROJECT_NAME: str = "FootprintIQ"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # ── Server ───────────────────────────────────────────────────
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ── Security ─────────────────────────────────────────────────
    SECRET_KEY: SecretStr = SecretStr("change-me-in-production-use-openssl-rand-hex-32")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    BCRYPT_ROUNDS: int = 12

    # ── CORS ─────────────────────────────────────────────────────
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # ── Database ─────────────────────────────────────────────────
    DATABASE_URL: str = "postgresql://footprintiq:footprintiq@localhost:5432/footprintiq"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30

    # ── Redis ────────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_TTL_DEFAULT: int = 3600  # 1 hour

    # ── AI / Anthropic ───────────────────────────────────────────
    ANTHROPIC_API_KEY: str = ""
    AI_MODEL: str = "claude-sonnet-4-20250514"
    AI_MAX_TOKENS: int = 2048
    AI_TEMPERATURE: float = 0.7
    AI_RATE_LIMIT_PER_HOUR: int = 100

    # ── Pinecone (Vector DB) ─────────────────────────────────────
    PINECONE_API_KEY: str = ""
    PINECONE_ENVIRONMENT: str = "us-east-1"
    PINECONE_INDEX_NAME: str = "footprintiq-knowledge"
    PINECONE_DIMENSION: int = 1536

    # ── Google OAuth ─────────────────────────────────────────────
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:3000/auth/callback"

    # ── AWS S3 ───────────────────────────────────────────────────
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str = "footprintiq-assets"

    # ── Logging ──────────────────────────────────────────────────
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }

    @model_validator(mode="after")
    def _validate_secret_key(self) -> "Settings":
        """Reject default SECRET_KEY in non-development environments."""
        default = "change-me-in-production-use-openssl-rand-hex-32"
        if (
            self.ENVIRONMENT != "development"
            and self.SECRET_KEY.get_secret_value() == default
        ):
            raise ValueError(
                "SECRET_KEY must be changed from the default in production. "
                "Generate one with: openssl rand -hex 32"
            )
        return self


settings = Settings()
