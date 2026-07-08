import redis
import ssl
from config import settings

def get_redis_client():
    if settings.redis_url.startswith("rediss://"):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        return redis.from_url(
            settings.redis_url,
            decode_responses=True,
            ssl_context=ssl_context
        )
    return redis.from_url(
        settings.redis_url,
        decode_responses=True
    )

redis_client = get_redis_client()

CACHE_TTL = 3600

def get_cached_url(slug: str):
    try:
        return redis_client.get(f"url:{slug}")
    except Exception:
        return None

def cache_url(slug: str, original_url: str):
    try:
        redis_client.setex(
            f"url:{slug}",
            CACHE_TTL,
            original_url
        )
    except Exception:
        pass

def invalidate_cache(slug: str):
    try:
        redis_client.delete(f"url:{slug}")
    except Exception:
        pass

def check_rate_limit(user_id: str, tier: str) -> bool:
    try:
        key = f"rate:{user_id}"
        limit = 100 if tier == "free" else 10000
        current = redis_client.get(key)
        if current is None:
            redis_client.setex(key, 86400, 1)
            return True
        if int(current) >= limit:
            return False
        redis_client.incr(key)
        return True
    except Exception:
        # If Redis fails, allow the request
        return True