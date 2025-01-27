from sqlalchemy.event import listens_for
from app_new.db.models.user import User
from app_new.events.redis_publisher import publish_user_created_event
import asyncio


@listens_for(User, "after_insert")
def after_user_insert(mapper, connection, target):
    asyncio.create_task(publish_user_created_event(target.id, target.name))


@listens_for(User, "after_update")
def after_user_update(mapper, connection, target):
    asyncio.create_task(publish_user_created_event(target.id, target.name))
