import logging

from aiogram.types import Update
from fastapi import APIRouter
from starlette.requests import Request

from app.bot.bot import dp, BotManager

logger = logging.getLogger(__name__)
router = APIRouter(prefix="", tags=["Telegram"])


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
