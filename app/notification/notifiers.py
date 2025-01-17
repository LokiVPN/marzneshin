from enum import Enum
from app.db import GetDB, crud
from app.notification import (
    get_notification_strategy,
    get_notification_manager,
)


async def notify(action: Enum, **kwargs) -> None:
    try:
        manager = get_notification_manager()
        with GetDB() as db:
            if not (notification_template := crud.get_notification_by_label(db, action.value)):
                raise ValueError(f"Notification template for {action} not found")
    except ValueError:
        return

    strategy = get_notification_strategy()
    notification = strategy.create_notification(action=action, message=notification_template.message, **kwargs)

    await manager.send_notification(notification)
