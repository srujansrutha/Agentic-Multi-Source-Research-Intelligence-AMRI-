import redis
from app.core.config import settings
import json
from typing import Optional

class RedisCache:
    def __init__(self):
        self.client = redis.from_url(settings.REDIS_URL, decode_responses=True)

    def get_cache(self, query: str) -> Optional[dict]:
        """Retrieve cached research result for a query."""
        cached_data = self.client.get(f"research:{query}")
        if cached_data:
            return json.loads(cached_data)
        return None

    def set_cache(self, query: str, response: dict, expire: int = 86400):
        """Cache research result for 24 hours."""
        self.client.setex(f"research:{query}", expire, json.dumps(response))

# Global instance
redis_client = RedisCache()
