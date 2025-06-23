from functools import lru_cache
from app.config import settings
from redis import Redis

@lru_cache
def get_redis_client() -> Redis:
    return Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)