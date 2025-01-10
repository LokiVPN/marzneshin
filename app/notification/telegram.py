import logging
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramAPIError

from app.bot.bot import BotManager
from app.config.env import (
    TELEGRAM_ADMIN_ID,
    TELEGRAM_LOGGER_CHANNEL_ID,
)
from app.models.notification import Notification
from app.notification.helper import create_text

logger = logging.getLogger(__name__)


async def send_message(
    message: str,
    parse_mode=ParseMode.HTML,
):
    if not (bot := await BotManager.get_instance()):
        return

    for recipient_id in (TELEGRAM_ADMIN_ID or []) + [
        TELEGRAM_LOGGER_CHANNEL_ID
    ]:
        if not recipient_id:
            continue
        try:
            await bot.send_message(
                recipient_id,
                message,
                parse_mode=parse_mode,
            )
        except TelegramAPIError as e:
            logger.error(e)


async def send_notification(notif: Notification):
    text = create_text(notif)
    await send_message(text)
