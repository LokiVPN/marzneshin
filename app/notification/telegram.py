import logging
from aiogram.exceptions import TelegramAPIError

from app.bot.manager import BotManager
from app.config.env import TELEGRAM_LOGGER_CHANNEL_ID
from app.models.notification import Notification, UserNotification
from app.templates import render_template_string

logger = logging.getLogger(__name__)


async def send_message(
    chat_id: int = None,
    message: str = "",
):
    if not (bot := await BotManager.get_instance()):
        return

    for recipient_id in (TELEGRAM_LOGGER_CHANNEL_ID or []) + [chat_id]:
        if not recipient_id:
            continue
        try:
            logger.info(f"Sending message to {recipient_id}: {message}")
            await bot.send_message(
                chat_id=recipient_id,
                text=message,
            )
        except TelegramAPIError as e:
            logger.error(e)


async def send_notification(notif: Notification):
    formatted_message = render_template_string(
        notif.message, notif.model_dump()
    )
    if isinstance(notif, UserNotification):
        await send_message(chat_id=notif.user.id, message=formatted_message)
    else:
        await send_message(message=formatted_message)
