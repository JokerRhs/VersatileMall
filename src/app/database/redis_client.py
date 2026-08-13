from redis.asyncio import Redis
from app.core.config import settings

redis: Redis | None = None

async def init_redis():
    global redis
    redis = Redis.from_url(settings.redis_dsn)

async def close_redis():
    global redis
    if redis:
        await redis.close()

def get_redis() -> Redis:
    if not redis:
        raise RuntimeError("Redis not initialized")
    return redis