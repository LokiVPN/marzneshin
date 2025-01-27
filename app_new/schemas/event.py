from enum import StrEnum
from typing import Literal

from pydantic import BaseModel
from datetime import datetime


class Event(StrEnum):
    USER_CREATED = "user_created"
    USER_UPDATED = "user_updated"
    USER_ACTIVATED = "user_activated"
    USER_DEACTIVATED = "user_deactivated"
    USER_DELETED = "user_deleted"
    USER_ENABLED = "user_enabled"
    USER_DISABLED = "user_disabled"
    DATA_USAGE_RESET = "data_usage_reset"
    SUBSCRIPTION_REVOKED = "subscription_revoked"
    REACHED_USAGE_PERCENT = "reached_usage_percent"
    REACHED_DAYS_LEFT = "reached_days_left"


class EventBase(BaseModel):
    event: Event
    timestamp: datetime


class UserEvent(EventBase):
    event: Literal[
        Event.USER_CREATED,
        Event.USER_UPDATED,
        Event.USER_ACTIVATED,
        Event.USER_DEACTIVATED,
        Event.USER_DELETED,
        Event.USER_ENABLED,
        Event.USER_DISABLED,
        Event.DATA_USAGE_RESET,
        Event.SUBSCRIPTION_REVOKED,
        Event.REACHED_USAGE_PERCENT,
        Event.REACHED_DAYS_LEFT,
    ]
    user_id: int
