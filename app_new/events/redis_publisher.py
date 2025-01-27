from functools import lru_cache

import redis.asyncio as redis
from app_new.core.config import get_settings
from app_new.schemas.event import UserCreatedEvent
from datetime import datetime

redis_op = get_settings().redis


@lru_cache(maxsize=128)
def get_redis_client(func):
    async def wrapper(*args, **kwargs):
        redis_client = redis.Redis(
            host=redis_op.host,
            port=redis_op.port,
            db=redis_op.db,
            password=redis_op.password,
        )
        return await func(redis_client, *args, **kwargs)

    return wrapper


@get_redis_client
async def publish_user_created_event(redis_client, user_id: int):
    event = UserCreatedEvent(
        event="user_created",
        user_id=user_id,
        timestamp=datetime.utcnow(),
    )
    await redis_client.publish("user_events", event.model_dump_json())
