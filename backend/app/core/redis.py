from redis import asyncio as aioredis

from .config import settings

redis_client: aioredis.Redis | None = None


async def get_redis() -> aioredis.Redis:
    """FastAPI dependency: get Redis client."""
    global redis_client
    if redis_client is None:
        redis_client = aioredis.from_url(
            settings.redis_url,
            decode_responses=True,
        )
    return redis_client


async def close_redis():
    """Close Redis connection on shutdown."""
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None
