import logging
from typing import Annotated

from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.web_app import safe_parse_webapp_init_data
from fastapi import APIRouter, HTTPException, Depends, Form
from starlette.responses import HTMLResponse

from app.bot.manager import BotManager
from app.bot.helper import create_invoice, get_prices
from app.db import crud, User
from app.dependencies import DBDep
from app.db.models import Settings
from app.models.settings import SubscriptionSettings
from app.models.telegram import (
    InvoiceLink,
    Currency,
    PricesResponse,
    InviteLink,
)
from app.models.user import UserResponse
from app.utils.share import generate_subscription_template

logger = logging.getLogger(__name__)
router = APIRouter(prefix="", tags=["Telegram"])


async def get_db_user(db: DBDep, auth: str = Form(alias="_auth", validation_alias="_auth", description="Telegram Init data")):
    bot = await BotManager.get_instance()
    if not bot:
        logger.error("Telegram bot is not initialized.")
        raise HTTPException(
            status_code=500, detail="Telegram bot is not initialized."
        )

    try:
        data = safe_parse_webapp_init_data(
            token=bot.token, init_data=auth
        )
    except ValueError:
        raise HTTPException(status_code=401, detail="Unauthorized")

    db_user = crud.get_user_by_id(db, data.user.id)
    return db_user


TGUserDep = Annotated[User, Depends(get_db_user)]


@router.post("/get_me", response_model=UserResponse)
async def get_me(user: TGUserDep):
    logger.info(f"User {user.id} requested his info")
    return user


@router.post("/sub")
async def get_user_subscription(user: TGUserDep, db: DBDep):
    logger.info(f"User {user.id} requested subscription")
    subscription_settings = SubscriptionSettings.model_validate(
        db.query(Settings.subscription).first()[0]
    )
    return HTMLResponse(
        generate_subscription_template(user, subscription_settings)
    )


@router.post("/prices", response_model=PricesResponse)
def prices(user: TGUserDep):
    """
    Get prices for the invoice
    """
    return {
        Currency.RUB: sum(l.amount for l in get_prices(Currency.RUB, 30)),
        Currency.XTR: sum(l.amount for l in get_prices(Currency.XTR, 30)),
    }


@router.post("/personal_link", response_model=InviteLink)
async def personal_link(user: TGUserDep):
    """
    Get a personal link for the user
    """
    bot = await BotManager.get_instance()
    if not bot:
        logger.error("Telegram bot is not initialized.")
        return

    start_link = await create_start_link(bot, str(user.id), encode=True)
    return InviteLink(link=start_link)


@router.post("/invoice", response_model=InvoiceLink)
async def generate_invoice(
    duration: Annotated[int, Form(ge=1, le=365, description="Продолжительность в днях")],
    user: TGUserDep,
    db: DBDep,
    currency: Annotated[Currency, Form(description="Валюта")] = Currency.RUB,
    is_subscription: Annotated[bool, Form(description="Ежемесячная оплата в XTR")] = False,
    is_link: Annotated[bool, Form(description="Вернуть ссылку или отправить в чате")] = True,
):
    """
    Generate an invoice for the user
    """
    if not (bot := await BotManager.get_instance()):
        logger.error("Telegram bot is not initialized.")
        return

    invoice_link = await create_invoice(
        bot,
        crud.get_user_by_id(db, user.id),
        currency,
        duration,
        is_subscription,
        is_link,
    )

    return InvoiceLink(link=invoice_link)
