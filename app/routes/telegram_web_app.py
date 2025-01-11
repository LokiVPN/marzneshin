import logging
from typing import Annotated

from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.web_app import safe_parse_webapp_init_data
from fastapi import APIRouter, HTTPException, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app.bot.bot import BotManager
from app.bot.helper import create_invoice, get_prices
from app.db import crud, User
from app.dependencies import DBDep
from app.db.models import Settings
from app.models.settings import SubscriptionSettings
from app.models.telegram import (
    CreateInvoice,
    InvoiceLink,
    Currency,
    PricesResponse,
    InviteLink,
)
from app.models.user import UserResponse
from app.templates import render_template
from app.utils.share import generate_subscription_template

logger = logging.getLogger(__name__)
router = APIRouter(prefix="", tags=["Telegram"])


@router.get("/")
async def web_app_init():
    return HTMLResponse(render_template("web.html"))


async def get_db_user(request: Request, db: DBDep):
    bot = await BotManager.get_instance()
    if not bot:
        logger.error("Telegram bot is not initialized.")
        raise HTTPException(status_code=500, detail="Telegram bot is not initialized.")

    data = await request.form()
    logger.info(f"Webapp init data: {data}")
    try:
        data = safe_parse_webapp_init_data(
            token=bot.token, init_data=data["_auth"]
        )
    except ValueError:
        raise HTTPException(status_code=401, detail="Unauthorized")

    db_user = crud.get_user_by_id(db, data.user.id)
    return db_user


TGUserDep = Annotated[User, Depends(get_db_user)]


@router.post("/get_me", response_model=UserResponse)
async def get_me(user: TGUserDep):
    logger.info(f"User {user.id} requested his info")
    return UserResponse.model_validate(user)


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
    user: TGUserDep,
    db: DBDep,
    new_invoice: CreateInvoice,
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
        new_invoice.currency,
        new_invoice.duration,
        new_invoice.is_subscription,
        new_invoice.is_link,
    )

    return InvoiceLink(link=invoice_link)
