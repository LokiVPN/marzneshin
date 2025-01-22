import os
from datetime import datetime

import yaml

from app.utils.system import readable_size


def to_yaml(obj):
    if not obj:
        return ""

    return yaml.dump(obj, allow_unicode=True, indent=2)


def exclude_keys(obj, *target_keys):
    return {key: val for key, val in obj.items() if key not in target_keys}


def only_keys(obj, *target_keys):
    return {key: val for key, val in obj.items() if key in target_keys}


def datetimeformat(dt):
    if isinstance(dt, int):
        dt = datetime.fromtimestamp(dt)
    formatted_datetime = dt.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_datetime


def env_override(value, key):
    return os.getenv(key, value)


def pluralize_ru(value: int | float | None, first: str, second: str, third: str):
    """
    Склонение слова по числу.

    :param value: Число
    :param first: Первая форма слова
    :param second: Вторая форма слова
    :param third: Третья форма слова
    """
    value = abs(int(value or 0))  # Берем модуль числа

    if 11 <= value % 100 <= 19:
        return third
    elif value % 10 == 1:
        return first
    elif 2 <= value % 10 <= 4:
        return second
    else:
        return third


CUSTOM_FILTERS = {
    "yaml": to_yaml,
    "except": exclude_keys,
    "only": only_keys,
    "datetime": datetimeformat,
    "bytesformat": readable_size,
    "pluralize_ru": pluralize_ru,
}
