import logging
from typing import Callable, Awaitable

from aiogram import Dispatcher, BaseMiddleware
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.types import Message
from sqlalchemy.orm import Session

from app.bot.helper import get_or_create_user
from app.bot.messages import (
    start_message,
    help_message,
    terms_of_service_message,
)
from app.db import crud, User
from app.db import GetDB

logger = logging.getLogger(__name__)
dp = Dispatcher()


class Middleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, any]], Awaitable[any]],
        event: Message,
        data: dict[str, any],
    ) -> any:
        with GetDB() as db:
            data["db"] = db
            data["user"] = crud.get_user_by_id(db, event.from_user.id)
        return await handler(event, data)


dp.message.outer_middleware(Middleware())


@dp.message(CommandStart(deep_link=True))
async def command_start__deep_handler(
    message: Message, command: CommandObject, db: Session, user: User
) -> None:
    """
    This handler receives messages with `/start` command
    """
    if not user:
        user = get_or_create_user(db, message.from_user, command.args)

    await message.answer(start_message(user.username))


@dp.message(CommandStart())
async def command_start_handler(
    message: Message, db: Session, user: User
) -> None:
    """
    This handler receives messages with `/start` command
    """
    if not user:
        user = get_or_create_user(db, message.from_user)

    await message.answer(start_message(user.username))


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    """
    This handler receives messages with `/help` command
    """
    await message.answer(help_message())


@dp.message(Command("terms"))
async def command_terms_handler(message: Message) -> None:
    """
    This handler receives messages with `/terms` command
    """
    await message.answer(terms_of_service_message())
