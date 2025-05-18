import os
import redis
import json
from typing import List, Dict, Any

class InMemoryStore:
    _redis = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, decode_responses=True)

    @classmethod
    def add_notification(cls, user_id: str, notification: Dict[str, Any]):
        key = f"notifications:{user_id}"
        cls._redis.rpush(key, json.dumps(notification))

    @classmethod
    def get_notifications(cls, user_id: str) -> List[Dict[str, Any]]:
        key = f"notifications:{user_id}"
        notifications = cls._redis.lrange(key, 0, -1)
        return [json.loads(n) for n in notifications] if notifications else []
