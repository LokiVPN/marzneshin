from datetime import datetime as dt, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from app.models.admin import Admin
from app.models.user import UserResponse


class Notification(BaseModel):
    created_at: float = dt.utcnow().timestamp()


class AdminNotif(Notification):
    pass


class UserNotification(Notification):
    user: UserResponse
    message: str

    class Action(str, Enum):
        user_created = "user_created"
        user_updated = "user_updated"
        user_activated = "user_activated"
        user_deactivated = "user_deactivated"
        user_deleted = "user_deleted"
        user_enabled = "user_enabled"
        user_disabled = "user_disabled"
        data_usage_reset = "data_usage_reset"
        subscription_revoked = "subscription_revoked"
        reached_usage_percent = "reached_usage_percent"
        reached_days_left = "reached_days_left"
        get_bonus = "get_bonus"
        custom = "custom"


class UserCreated(UserNotification):
    action: UserNotification.Action = UserNotification.Action.user_created
    by: Optional[Admin] = None


class UserUpdated(UserNotification):
    action: UserNotification.Action = UserNotification.Action.user_updated
    by: Optional[Admin] = None


class UserActivated(UserNotification):
    action: UserNotification.Action = UserNotification.Action.user_activated
    by: Optional[Admin] = None


class UserDeactivated(UserNotification):
    action: UserNotification.Action = UserNotification.Action.user_deactivated
    by: Optional[Admin] = None


class UserDeleted(UserNotification):
    action: UserNotification.Action = UserNotification.Action.user_deleted
    by: Admin


class UserEnabled(UserNotification):
    action: UserNotification.Action = UserNotification.Action.user_enabled
    by: Optional[Admin] = None


class UserDisabled(UserNotification):
    action: UserNotification.Action = UserNotification.Action.user_disabled
    by: Optional[Admin] = None


class UserDataUsageReset(UserNotification):
    action: UserNotification.Action = UserNotification.Action.data_usage_reset
    by: Optional[Admin] = None


class UserSubscriptionRevoked(UserNotification):
    action: UserNotification.Action = (
        UserNotification.Action.subscription_revoked
    )
    by: Admin


class ReachedUsagePercent(UserNotification):
    action: UserNotification.Action = (
        UserNotification.Action.reached_usage_percent
    )


class ReachedDaysLeft(UserNotification):
    action: UserNotification.Action = UserNotification.Action.reached_days_left


class GetBonus(UserNotification):
    action: UserNotification.Action = UserNotification.Action.get_bonus


class CustomNotification(UserNotification):
    action: UserNotification.Action = UserNotification.Action.custom


class DBNotificationTargetResponse(BaseModel):
    user: UserResponse
    sent_at: datetime | None
    skipped: bool = False

    model_config = ConfigDict(from_attributes=True)


class DBNotification(BaseModel):
    id: int | None = None
    message: str


class CreateDBNotification(DBNotification):
    label: str
    user_ids: list[int] = Field([])
    action: UserNotification.Action


class ModifyDBNotification(DBNotification):
    user_ids: list[int] = Field([])
    message: str | None = None


class DBNotificationResponse(DBNotification):
    id: int
    label: str
    action: UserNotification.Action
    created_at: datetime
    started_at: datetime | None
    finished_at: datetime | None
    user_ids: list[int]
    completed: bool

    model_config = ConfigDict(from_attributes=True)
