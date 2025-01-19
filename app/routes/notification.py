import asyncio
import logging
from datetime import datetime

from fastapi import APIRouter, Query
from fastapi import HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination.links import Page

from app.db import crud
from app.db.models import Notification, User, NotificationTarget
from app.dependencies import DBDep, AdminDep, SudoAdminDep, NotificationDep
from app.models.notification import (
    DBNotificationResponse,
    CreateDBNotification,
    ModifyDBNotification,
    UserNotification,
    DBNotificationTargetResponse,
)
from app.models.user import UserResponse, UserExpireStrategy
from app.notification import notify

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("", response_model=Page[DBNotificationResponse])
def get_notifications(db: DBDep, admin: AdminDep, label: str = Query(None)):
    query = db.query(Notification)

    if label:
        query = query.filter(Notification.label.ilike(f"%{label}%"))

    return paginate(query)


@router.post("", response_model=DBNotificationResponse)
def add_notification(
    new_notification: CreateDBNotification, db: DBDep, admin: SudoAdminDep
):
    """
    Add a new notification

    - **label** notification label
    - **message** notification message
    - **action** notification action
    - **user_ids** list of user ids
    """
    return crud.create_notification(db, new_notification)


@router.get("/{id}", response_model=DBNotificationResponse)
def get_notification(
    notification: NotificationDep, db: DBDep, admin: AdminDep
):
    """
    Get Notification information with id
    """
    return notification


@router.get("/{id}/users", response_model=Page[DBNotificationTargetResponse])
def get_notification_users(
    notification: NotificationDep, db: DBDep, admin: SudoAdminDep
):
    """
    Get notification users
    """
    query = db.query(NotificationTarget).filter(
        NotificationTarget.notification_id == notification.id
    )

    return paginate(query)


@router.post("/{id}/test", response_model=DBNotificationResponse)
async def test_notification(
    notification: NotificationDep, db: DBDep, admin: SudoAdminDep
):
    if admin.telegram_chat_id is None:
        raise HTTPException(
            status_code=400, detail="Admin has no telegram_chat_id"
        )
    fake_user = User(
        id=admin.telegram_chat_id,
        username=admin.username,
        expire_strategy=UserExpireStrategy.NEVER,
        key="",
        data_limit_reset_strategy="no_reset",
        is_telegram_premium=False,
        enabled=True,
        used_traffic=0,
        lifetime_used_traffic=0,
        created_at=datetime.utcnow(),
        activated=True,
    )
    asyncio.ensure_future(
        notify(
            action=notification.action,
            user=UserResponse.model_validate(fake_user),
            by=admin,
            message=notification.message,
        )
    )

    return notification


@router.post("/{id}/start", response_model=DBNotificationResponse)
async def start_notification(
    notification: NotificationDep, db: DBDep, admin: SudoAdminDep
):
    """
    Start Notification with id
    """
    if not len(notification.user_ids):
        raise HTTPException(
            status_code=400, detail="No users to send notification"
        )

    if notification.action != UserNotification.Action.custom:
        raise HTTPException(
            status_code=400, detail="Only custom notifications can be started"
        )

    for target in notification.targets:
        asyncio.ensure_future(
            notify(
                action=notification.action,
                message=notification.message,
                user=UserResponse.model_validate(target.user),
                by=admin,
            )
        )

    return notification


@router.put("/{id}", response_model=DBNotificationResponse)
def modify_notification(
    notification: NotificationDep,
    modification: ModifyDBNotification,
    db: DBDep,
    admin: SudoAdminDep,
):
    """
    Modify Notification with id
    """
    return crud.update_notification(db, notification, modification)


@router.delete("/{id}")
def remove_notification(
    notification: NotificationDep, db: DBDep, admin: SudoAdminDep
):
    """
    Remove Notification with id
    """
    return crud.remove_notification(db, notification)
