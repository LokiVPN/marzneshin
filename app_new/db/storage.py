import contextlib
from typing import AsyncIterator

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
    create_async_engine,
)

from app_new.core.config import get_settings


class DatabaseSessionManager:
    def __init__(self, _engine: AsyncEngine) -> None:
        self._engine: AsyncEngine = _engine
        self._sessionmaker = async_sessionmaker(
            bind=self._engine,
            autocommit=False,
            expire_on_commit=False,
        )

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        else:
            await session.commit()
        finally:
            await session.close()


class Storage:
    _instance = None
    __initialized: bool

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False

        return cls._instance

    def __init__(self) -> None:
        if self.__initialized:
            return

        self.session_manager = DatabaseSessionManager(
            self.new_async_engine(get_settings().postgres.synapse.dsn)
        )
        self.__initialized = True

    @staticmethod
    def new_async_engine(dsn: str) -> AsyncEngine:
        return create_async_engine(url=dsn, poolclass=NullPool)


def get_db() -> Storage:
    return Storage()
