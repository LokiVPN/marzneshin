import logging
from typing import Callable, Awaitable

from aiogram import Dispatcher, Bot, BaseMiddleware
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, LabeledPrice
from aiogram.utils.markdown import hbold
from sqlalchemy.orm import Session

from app.bot.helper import get_or_create_user
from app.config import (
    TELEGRAM_API_TOKEN,
    TELEGRAM_PROXY_URL,
    TELEGRAM_PAYMENT_TOKEN,
)
from app.db import crud, User
from app.db import GetDB
from app.models.user import (
    UserCreate,
    UserExpireStrategy,
    UserDataUsageResetStrategy,
)


logger = logging.getLogger(__name__)
dp = Dispatcher()


class DbMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        with GetDB() as db:
            self.db = db

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, any]], Awaitable[any]],
        event: Message,
        data: dict[str, any],
    ) -> any:
        data["db"] = self.db
        data["user"] = crud.get_user_by_id(self.db, event.from_user.id)
        return await handler(event, data)


dp.message.outer_middleware(DbMiddleware())


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
            except:
                logger.error("Telegram API token is not valid.")
        return cls._instance


@dp.message(CommandStart(deep_link=True))
async def command_start__deep_handler(
    message: Message, command: CommandObject, db: Session, user: User
) -> None:
    """
    This handler receives messages with `/start` command
    """
    if not user:
        user = get_or_create_user(db, message.from_user, command.args)

    await message.answer(f"Hello deep, {hbold(user.username)}! {command.args}")


@dp.message(CommandStart())
async def command_start_handler(
    message: Message, db: Session, user: User
) -> None:
    """
    This handler receives messages with `/start` command
    """
    if not user:
        user = get_or_create_user(db, message.from_user)

    link = await message.bot.create_invoice_link(
        title="Test invoice",
        description="Test invoice description",
        payload="payload",
        currency="RUB",
        provider_token=TELEGRAM_PAYMENT_TOKEN,
        prices=[
            LabeledPrice(label="Test price", amount=10000),
        ],
    )
    await message.answer(f"Hello, {hbold(user.username)}! {link}")
