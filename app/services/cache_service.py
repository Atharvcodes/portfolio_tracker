import redis
import json
from typing import Optional, Any
from app.config import settings

try:
    redis_client = redis.from_url(settings.redis_url, decode_responses=True)
    redis_client.ping()
    print("Redis connected successfully")
except Exception as e:
    print(f"Redis connection failed: {e}. Caching disabled.")
    redis_client = None

def get_cache(key: str) -> Optional[Any]:
    if not redis_client:
        return None
    
    try:
        value = redis_client.get(key)
        if value:
            return json.loads(value)
        return None
    except Exception as e:
        print(f"Cache get error: {e}")
        return None

def set_cache(key: str, value: Any, ttl: int = settings.cache_ttl) -> bool:
    if not redis_client:
        return False
    
    try:
        redis_client.setex(key, ttl, json.dumps(value, default=str))
        return True
    except Exception as e:
        print(f"Cache set error: {e}")
        return False

def invalidate_cache(pattern: str) -> bool:
    if not redis_client:
        return False
    
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
        return True
    except Exception as e:
        print(f"Cache invalidate error: {e}")
        return False
