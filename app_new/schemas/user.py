import secrets
from datetime import datetime
from typing import Annotated

from pydantic import (
    BaseModel,
    StringConstraints,
    Field,
    ConfigDict,
    model_validator,
)
from app_new.core.common.user import (
    USERNAME_REGEXP,
    UserExpireStrategy,
    UserDataUsageResetStrategy,
)


class User(BaseModel):
    id: int | None = None
    username: Annotated[
        str, StringConstraints(to_lower=True, pattern=USERNAME_REGEXP)
    ]
    expire_strategy: UserExpireStrategy
    expire_date: datetime | None = Field(None)
    usage_duration: int | None = Field(None)
    activation_deadline: datetime | None = Field(None)
    key: str = Field(default_factory=lambda: secrets.token_hex(16))
    data_limit: int | None = Field(
        ge=0, default=None, description="data_limit can be 0 or greater"
    )
    data_limit_reset_strategy: UserDataUsageResetStrategy = (
        UserDataUsageResetStrategy.NO_RESET
    )
    note: Annotated[str, Field(max_length=500)] | None = None
    sub_updated_at: datetime | None = Field(None)
    sub_last_user_agent: str | None = Field(None)
    online_at: datetime | None = Field(None)
    invited_by: int | None = Field(None)
    is_telegram_premium: bool = False
    last_payment_at: datetime | None = Field(None)
    last_telegram_payment_charge_id: str | None = Field(None)
    last_provider_payment_charge_id: str | None = Field(None)

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def validate_expiry(self):
        if self.expire_strategy == UserExpireStrategy.START_ON_FIRST_USE:
            if not self.usage_duration:
                raise ValueError(
                    "User expire_strategy cannot be start_on_first_use without a valid usage_duration."
                )

            # Set expire_date to None if expire_strategy is START_ON_FIRST_USE
            self.expire_date = None

        elif self.expire_strategy == UserExpireStrategy.FIXED_DATE:
            if not self.expire_date:
                raise ValueError(
                    "User expire_strategy cannot be fixed_date without a valid expire date."
                )

            # Set usage_duration and activation_deadline to None if expire_strategy is START_ON_FIRST_USE
            self.usage_duration = None
            self.activation_deadline = None

        elif self.expire_strategy == UserExpireStrategy.NEVER:
            # Set expire_date, usage_duration and activation_deadline to None if expire_strategy is NEVER
            self.expire_date = None
            self.usage_duration = None
            self.activation_deadline = None

        return self
