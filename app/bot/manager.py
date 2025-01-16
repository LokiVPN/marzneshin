import logging

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

from app.config import TELEGRAM_API_TOKEN, TELEGRAM_PROXY_URL


logger = logging.getLogger(__name__)


class BotManager:
    _instance = None

    @classmethod
    async def get_instance(cls):
        if cls._instance is None and TELEGRAM_API_TOKEN:
            if TELEGRAM_PROXY_URL:
                session = AiohttpSession(proxy=TELEGRAM_PROXY_URL)
            else:
                session = None

            cls._instance = Bot(
                token=TELEGRAM_API_TOKEN,
                default=DefaultBotProperties(parse_mode=ParseMode.HTML),
                session=session,
            )
            try:
                await cls._instance.get_me()
                await cls._instance.set_webhook(
                    url="https://loki-connect.ru/bot/webhook"
                )
            except:
                logger.error("Telegram API token is not valid.")
        return cls._instance