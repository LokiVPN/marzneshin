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


class CreateInvoice(BaseModel):
    currency: Currency = Field(Currency.RUB)
    duration: Annotated[int, Field(ge=1, le=365)] = Field(1)
    is_subscription: bool = Field(False)
    is_link: bool = Field(False)


class Link(BaseModel):
    link: HttpUrl


class InviteLink(Link): ...


class InvoiceLink(Link): ...
