import logging
from aiogram.types import Update
from fastapi import APIRouter
from starlette.requests import Request

from app.bot.bot import dp, BotManager
from app.bot.helper import create_invoice
from app.db import crud
from app.dependencies import AdminDep, DBDep, UserDep
from app.models.telegram import CreateInvoice, InvoiceLink

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/telegram", tags=["Telegram"])


@router.post("/webhook")
async def telegram_webhook(request: Request):
    """
    Telegram webhook endpoint for receiving messages from Telegram.
    """
    if not (bot := await BotManager.get_instance()):
        logger.error("Telegram bot is not initialized.")
        return

    update = Update.model_validate(await request.json(), context={"bot": bot})

    await dp.feed_update(bot, update)

    return {"status": "ok"}


@router.post("/{user_id}/invoice", response_model=InvoiceLink)
async def generate_invoice(
    user_id: int,
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
        crud.get_user_by_id(db, user_id),
        new_invoice.currency,
        new_invoice.duration,
        new_invoice.is_subscription,
        new_invoice.is_link,
    )

    return InvoiceLink(link=invoice_link)
