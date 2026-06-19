"""
Redis cache client with connection pooling.
Provides cache-aside, write-through, and TTL-based invalidation patterns.
"""

import json
from typing import Any, Optional

import redis.asyncio as redis

from app.core.config import settings


class RedisCache:
    """Async Redis cache wrapper with JSON serialization."""

    def __init__(self):
        self._redis: Optional[redis.Redis] = None

    async def connect(self):
        """Initialize Redis connection pool."""
        self._redis = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            max_connections=20,
        )

    async def disconnect(self):
        """Close Redis connection."""
        if self._redis:
            await self._redis.close()

    @property
    def client(self) -> redis.Redis:
        if self._redis is None:
            raise RuntimeError("Redis not connected. Call connect() first.")
        return self._redis

    # ── Core Operations ──────────────────────────────────────────

    async def get(self, key: str) -> Optional[Any]:
        """Get a value from cache, deserializing JSON."""
        value = await self.client.get(key)
        if value is not None:
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value
        return None

    async def set(
        self, key: str, value: Any, ttl: Optional[int] = None
    ) -> None:
        """Set a value in cache with optional TTL (seconds)."""
        serialized = json.dumps(value, default=str)
        if ttl:
            await self.client.setex(key, ttl, serialized)
        else:
            await self.client.set(key, serialized)

    async def delete(self, key: str) -> None:
        """Delete a key from cache."""
        await self.client.delete(key)

    async def exists(self, key: str) -> bool:
        """Check if a key exists."""
        return bool(await self.client.exists(key))

    async def increment(self, key: str, ttl: Optional[int] = None) -> int:
        """Increment a counter. Sets TTL on first increment."""
        val = await self.client.incr(key)
        if val == 1 and ttl:
            await self.client.expire(key, ttl)
        return val

    async def get_ttl(self, key: str) -> int:
        """Get remaining TTL for a key."""
        return await self.client.ttl(key)

    # ── Pattern-based Operations ─────────────────────────────────

    async def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching a pattern."""
        count = 0
        async for key in self.client.scan_iter(match=pattern):
            await self.client.delete(key)
            count += 1
        return count

    # ── Cache Key Builders ───────────────────────────────────────

    @staticmethod
    def user_profile_key(user_id: str) -> str:
        return f"user:{user_id}:profile"

    @staticmethod
    def user_carbon_key(user_id: str) -> str:
        return f"user:{user_id}:carbon:latest"

    @staticmethod
    def user_recommendations_key(user_id: str) -> str:
        return f"user:{user_id}:recommendations"

    @staticmethod
    def conversation_key(conversation_id: str) -> str:
        return f"conversation:{conversation_id}:messages"

    @staticmethod
    def leaderboard_key(board_type: str, period: str) -> str:
        return f"leaderboard:{board_type}:{period}"

    @staticmethod
    def rate_limit_key(user_id: str, resource: str) -> str:
        return f"rate:{resource}:{user_id}"


# Singleton instance
cache = RedisCache()
