from enum import Enum
from typing import Annotated

from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
)


class Currency(str, Enum):
    RUB = "RUB"
    XTR = "XTR"


class PricesResponse(BaseModel):
    RUB: int
    XTR: int


class Link(BaseModel):
    link: HttpUrl


class InviteLink(Link): ...


class InvoiceLink(Link): ...
