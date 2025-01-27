from functools import lru_cache
from pathlib import Path

from aiogram.enums import Currency
from pydantic import SecretStr, BaseModel, model_validator, HttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_DIR = Path(__file__).parent.parent.parent


class DatabaseSettings(BaseModel):
    dsn = Field(
        None,
        description="DSN для подключения к базе данных",
    )
    connection_pool_size: int = Field(
        10,
        description="Размер пула соединений с базой данных",
    )
    connection_max_overflow: int = Field(
        -1,
        description="Максимальное количество соединений, которые могут быть созданы в пуле",
    )

    @property
    def is_sqlite(self):
        return self.dsn.startswith("sqlite")


class RedisSettings(BaseModel):
    username: str
    password: str
    db: int
    cache_expires: int

    host: str
    port: int


class SentrySettings(BaseModel):
    dsn: str
    environment: str


class BotSettings(BaseModel):
    class Payment(BaseModel):
        provider_token: SecretStr = Field(
            description="Токен провайдера",
        )
        prices: dict[Currency, int] = Field(
            {
                "RUB": 350,
                "XTR": 1.5,
            },
            description="Цены на подписку",
        )

        @property
        def available_currencies(self):
            return list(self.prices.keys())

    proxy: str = Field(
        None,
        description="Прокси для подключения к Telegram",
    )
    token: SecretStr = Field(
        description="Токен бота",
    )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{PROJECT_DIR}/.env",
        case_sensitive=False,
        extra="ignore",
        env_nested_delimiter="__",
        hide_input_in_errors=True,
    )

    db: DatabaseSettings
    redis: RedisSettings
    sentry: SentrySettings
    bot: BotSettings


@lru_cache(maxsize=128)
def get_settings() -> Settings:
    return Settings()  # type: ignore
