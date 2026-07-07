import redis
from config import settings

redis_client = redis.from_url(
    settings.redis_url,
    decode_responses=True,
    ssl_cert_reqs=None
)

CACHE_TTL = 3600

def get_cached_url(slug: str):
    return redis_client.get(f"url:{slug}")

def cache_url(slug: str, original_url: str):
    redis_client.setex(
        f"url:{slug}",
        CACHE_TTL,
        original_url
    )

def invalidate_cache(slug: str):
    redis_client.delete(f"url:{slug}")

def check_rate_limit(user_id: str, tier: str) -> bool:
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