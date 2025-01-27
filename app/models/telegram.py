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


class Price(BaseModel):
    duration: int
    price: int
    discount_percent: int

    @property
    def price_with_discount(self):
        return self.price - (self.price * self.discount_percent) / 100


class PricesResponse(BaseModel):
    RUB: list[Price]
    XTR: list[Price]


class Link(BaseModel):
    link: HttpUrl


class InviteLink(Link): ...


class InvoiceLink(Link): ...
