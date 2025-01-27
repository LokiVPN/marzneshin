from enum import StrEnum
from typing import Final

USERNAME_REGEXP = r"^\w{3,32}$"


class UserStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class UserDataUsageResetStrategy(StrEnum):
    NO_RESET: Final = "no_reset"
    DAY: Final = "day"
    WEEK: Final = "week"
    MONTH: Final = "month"
    YEAR: Final = "year"


class UserExpireStrategy(StrEnum):
    NEVER: Final = "never"
    FIXED_DATE = "fixed_date"
    START_ON_FIRST_USE = "start_on_first_use"
