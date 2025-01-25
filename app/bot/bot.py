import logging
from datetime import timedelta, datetime
from enum import unique
from typing import Callable, Awaitable

from aiogram import Dispatcher, BaseMiddleware, F, Bot
from aiogram.enums import ContentType
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    Message,
    PreCheckoutQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
    CopyTextButton,
    CallbackQuery,
)
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app import marznode
from app.bot.helper import (
    get_or_create_user,
    decode_invoice_payload,
    create_invoice,
)
from app.config import REFERRAL_BONUS_DAYS_PERCENT
from app.db import crud, User
from app.db import GetDB
from app.models.telegram import Currency
from app.models.user import UserResponse
from app.templates import render_template_string

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
            data["user_db"] = crud.get_user_by_id(db, event.from_user.id)
        return await handler(event, data)


dp.message.outer_middleware(Middleware())


@dp.message(CommandStart(deep_link=True))
async def command_start__deep_handler(
    message: Message, command: CommandObject, db: Session, user_db: User = None
) -> None:
    """
    This handler receives messages with `/start` command
    """
    if not user_db:
        user_db = get_or_create_user(db, message.from_user, command.args)

    user = UserResponse.model_validate(user_db)

    if template := crud.get_notification_by_label(db, "bot.start"):
        await message.answer(
            render_template_string(template.message, {"user": user}),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Открыть приложение",
                            web_app=WebAppInfo(
                                url="https://loki-connect.ru/webapp/"
                            ),
                        ),
                        InlineKeyboardButton(
                            text="Скопировать подписку",
                            copy_text=CopyTextButton(
                                text=f"https://loki-connect.ru{user.subscription_url}"
                            ),
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="Реферальная ссылка",
                            copy_text=CopyTextButton(
                                text=await create_start_link(
                                    message.bot, str(user.id), encode=True
                                )
                            ),
                        )
                    ],
                ]
            ),
        )
    else:
        logger.error("Template not found")


@dp.message(CommandStart())
async def command_start_handler(
    message: Message, db: Session, user_db: User = None
) -> None:
    """
    This handler receives messages with `/start` command
    """
    logger.info(
        f"User {message.from_user.id} started the bot, {user_db.username}"
    )
    if not user_db:
        user_db = get_or_create_user(db, message.from_user)

    user = UserResponse.model_validate(user_db)

    if template := crud.get_notification_by_label(db, "bot.start"):
        await message.answer(
            render_template_string(template.message, {"user": user}),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Открыть приложение",
                            web_app=WebAppInfo(
                                url="https://loki-connect.ru/webapp/"
                            ),
                        ),
                        InlineKeyboardButton(
                            text="Скопировать подписку",
                            copy_text=CopyTextButton(
                                text=f"https://loki-connect.ru{user.subscription_url}"
                            ),
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="Реферальная ссылка",
                            copy_text=CopyTextButton(
                                text=await create_start_link(
                                    message.bot, str(user.id), encode=True
                                )
                            ),
                        )
                    ],
                ]
            ),
        )
    else:
        logger.error("Template not found")


@dp.message(Command("help"))
async def command_help_handler(
    message: Message, db: Session, user_db: User
) -> None:
    """
    This handler receives messages with `/help` command
    """
    if template := crud.get_notification_by_label(db, "bot.help"):
        await message.answer(
            render_template_string(
                template.message,
                {"user": UserResponse.model_validate(user_db)},
            )
        )
    else:
        logger.error("Template not found")


@dp.message(Command("terms"))
async def command_terms_handler(
    message: Message, db: Session, user_db: User
) -> None:
    """
    This handler receives messages with `/terms` command
    """
    if template := crud.get_notification_by_label(db, "bot.terms"):
        await message.answer(
            render_template_string(
                template.message,
                {"user": UserResponse.model_validate(user_db)},
            )
        )
    else:
        logger.error("Template not found")


@dp.pre_checkout_query()
async def process_pre_checkout_query(
    pre_checkout_query: PreCheckoutQuery, bot: Bot
):
    with GetDB() as db:
        if not crud.get_user_by_id(db, pre_checkout_query.from_user.id):
            logger.error(f"User {pre_checkout_query.from_user.id} not found")
            await bot.answer_pre_checkout_query(
                pre_checkout_query.id,
                ok=False,
                error_message="Пользователь не найден",
            )
            return
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(
    message: Message, db: Session, user_db: User
):
    try:
        user_id, _, duration = decode_invoice_payload(
            message.successful_payment.invoice_payload
        )
        user_db = crud.get_user_by_id(db, user_id)
        if not user_db:
            raise ValueError(f"User {user_id} not found")
        user_db = crud.extend_user_sub(
            db,
            user_db,
            timedelta(days=duration),
            message.successful_payment.provider_payment_charge_id,
            message.successful_payment.telegram_payment_charge_id,
        )
        marznode.operations.update_user(user=user_db)
        if user_db.invited_by:
            inviter = crud.get_user_by_id(db, user_db.invited_by)
            if inviter and (
                template := crud.get_notification_by_label(db, "bot.invite")
            ):
                inviter = crud.extend_user_sub(
                    db,
                    inviter,
                    timedelta(
                        days=int(
                            duration
                            * (100 - REFERRAL_BONUS_DAYS_PERCENT)
                            / 100
                        )
                    ),
                )
                await message.bot.send_message(
                    chat_id=inviter.id,
                    text=render_template_string(
                        template.message,
                        {
                            "from": UserResponse.model_validate(user_db),
                            "user": UserResponse.model_validate(inviter),
                        },
                    ),
                )
        await message.bot.delete_message(user_id, message.message_id - 1)
        # TODO: уведомление об реактивации
    except Exception as e:
        logger.error(e)
        await message.answer("Упс, что-то пошло не так...")


class PaymentCallback(CallbackData, prefix="payment"):
    user_id: int
    duration: int


@dp.message(Command("payments"))
async def command_payments_handler(
    message: Message, db: Session, user_db: User
) -> None:
    """
    This handler receives messages with `/payments` command
    """
    if template := crud.get_notification_by_label(db, "bot.payments"):
        builder = InlineKeyboardBuilder()
        for duration in [30, 90, 180, 365]:
            builder.button(
                text=f"{duration} дней",
                callback_data=PaymentCallback(
                    user_id=user_db.id, duration=duration
                ),
            )

        await message.answer(
            render_template_string(
                template.message,
                {"user": UserResponse.model_validate(user_db)},
            ),
            reply_markup=builder.as_markup(),
        )
    else:
        logger.error("Template not found")


@dp.callback_query(PaymentCallback.filter())
async def process_payment_callback(
    query: CallbackQuery,
    callback_data: PaymentCallback,
):
    with GetDB() as db:
        user_db = crud.get_user_by_id(db, callback_data.user_id)
        if not user_db:
            logger.error(f"User {query.from_user.id} not found")
            return

        try:
            await create_invoice(
                query.bot, user_db, Currency.RUB, callback_data.duration
            )
        except Exception as e:
            logger.error(e)
            await query.answer("Упс, что-то пошло не так...")
