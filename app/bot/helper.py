import asyncio
from datetime import datetime, timedelta
import logging
from aiogram.utils.payload import decode_payload, encode_payload
from sqlalchemy.orm import Session
from aiogram import types, Bot

from app import marznode
from app.config import TELEGRAM_PAYMENT_TOKEN
from app.db import crud, User
from app.models.notification import UserNotification
from app.models.telegram import Currency
from app.models.user import (
    UserCreate,
    UserExpireStrategy,
    UserDataUsageResetStrategy,
    UserModify,
)
from app.notification import notify

logger = logging.getLogger(__name__)


def get_or_create_user(
    db: Session, tg_user: types.User, deep_link_payload: str = None
) -> User:
    if not (db_user := crud.get_user_by_id(db, tg_user.id)):
        services = crud.get_public_services(db)
        new_user = UserCreate(
            id=tg_user.id,
            username=tg_user.username,
            is_telegram_premium=tg_user.is_premium or False,
            service_ids=[service.id for service in services],
            expire_strategy=UserExpireStrategy.FIXED_DATE,
            expire_date=datetime.utcnow()
            + timedelta(days=2),  # TODO: Get from env
            data_limit=500 * 1024 * 1024 * 1024,  # TODO: Get from env
            data_limit_reset_strategy=UserDataUsageResetStrategy.month,
        )

        if deep_link_payload:
            logger.info(
                f"User {tg_user.id} was invited by {deep_link_payload}"
            )
            invitee_id = int(decode_payload(deep_link_payload))
            if crud.get_user_by_id(db, invitee_id):
                new_user.invited_by = invitee_id

        db_user = crud.create_user(db, new_user)
        marznode.operations.update_user(user=db_user)

        action = UserNotification.Action.user_created
        if template := crud.get_notification_by_label(db, action.value):
            asyncio.ensure_future(
                notify(
                    action=action,
                    message=template.message,
                    user=db_user,
                    by=None,
                )
            )
    else:
        # обновляем его данные если они изменились
        upd_user = UserModify(
            username=tg_user.username,
            is_telegram_premium=tg_user.is_premium or False,
        )
        if (
            upd_user.username != tg_user.username
            or upd_user.is_telegram_premium != tg_user.is_premium
        ):
            crud.update_user(
                db,
                db_user,
                upd_user,
            )
            marznode.operations.update_user(user=db_user)

    return db_user


def plural_days(days: int):
    if days % 10 == 1 and days % 100 != 11:
        return f"{days} день"
    return (
        f"{days} дня"
        if 2 <= days % 10 <= 4 and (days % 100 < 10 or days % 100 >= 20)
        else f"{days} дней"
    )


def encode_invoice_payload(
    user_id: int, currency: Currency, duration: int
) -> str:
    return encode_payload(":".join([user_id, currency.value, str(duration)]))


def decode_invoice_payload(payload: str) -> tuple[int, Currency, int]:
    payload_decoded = decode_payload(payload).split(":")
    duration = int(payload_decoded.pop())
    currency = Currency(payload_decoded.pop())
    user_id = int(payload_decoded.pop())
    return user_id, currency, duration


def get_prices(currency: Currency, duration: int) -> list[types.LabeledPrice]:
    cost_per_day = 3.5  # TODO: Get from env
    multiply = 100 if currency == Currency.RUB else 0.5

    return [
        types.LabeledPrice(
            label=f"Оплата на {plural_days(duration)}",
            amount=int(cost_per_day * multiply * duration),
        )
    ]


async def create_invoice(
    bot: Bot,
    user: User,
    currency: Currency,
    duration: int,
    is_subscription: bool = False,
    is_link: bool = False,
) -> str:
    if is_subscription and currency != Currency.XTR:
        raise ValueError("Invalid currency for subscription")

    if is_subscription and duration != 30:
        raise ValueError("Invalid duration for subscription")

    title = "Доступ к VPN"
    description = f"Оплата за использование VPN на {plural_days(duration)}"

    if currency in [Currency.XTR, Currency.RUB]:
        if is_link:
            return await bot.create_invoice_link(
                title=title,
                description=description,
                payload=encode_invoice_payload(user.id, currency, duration),
                subscription_period=2592000 if is_subscription else None,
                currency=currency.value,
                prices=get_prices(currency, duration),
                provider_token=(
                    TELEGRAM_PAYMENT_TOKEN
                    if currency == Currency.RUB
                    else None
                ),
                max_tip_amount=10000 if currency == Currency.RUB else None,
            )
        await bot.send_invoice(
            chat_id=user.id,
            title=title,
            description=description,
            payload=encode_invoice_payload(user.id, currency, duration),
            currency=currency.value,
            prices=get_prices(currency, duration),
            provider_token=(
                TELEGRAM_PAYMENT_TOKEN if currency == Currency.RUB else None
            ),
            max_tip_amount=10000 if currency == Currency.RUB else None,
        )

        return ""

    else:
        raise ValueError("Invalid currency")


async def get_chat_info(bot: Bot, chat_id: int):
    """
    Get chat info by chat_id для импорта из marzban
    """
    try:
        return await bot.get_chat(chat_id)
    except Exception as e:
        logger.error(f"Failed to get chat info: {e}")
        return None
