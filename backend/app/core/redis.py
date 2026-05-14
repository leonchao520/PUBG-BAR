from .config import settings

redis_client = None


async def get_redis():
    """FastAPI dependency: get Redis client. In dev mode, yield None."""
    global redis_client
    if settings.dev_mode:
        yield None
        return

    if redis_client is None:
        from redis import asyncio as aioredis

        _client = aioredis.from_url(
            settings.redis_url,
            decode_responses=True,
        )
        # store in a non-None attribute
        globals()["_redis"] = _client
        yield _client
    else:
        yield redis_client


async def close_redis():
    """Close Redis connection on shutdown."""
    _client = globals().get("_redis")
    if _client:
        await _client.close()
