from typing import AsyncGenerator, Awaitable, ParamSpec, TypeVar
from collections.abc import Callable

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
)

from app.api import load_settings


P = ParamSpec("P")
R = TypeVar("R")


class CreateSession:
    def __init__(self, db_url: str) -> None:
        self.db_url = db_url

    async def __call__(self) -> Callable[P, Awaitable[R]]:
        return await self._async_session()

    def _create_engine(self) -> AsyncEngine:
        return create_async_engine(
            url=load_settings.db_url,
            future=True,
            echo=True,
        )

    async def _create_session_factory(
        self,
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            self._create_engine(),
            autoflush=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    async def _async_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Dependency for getting async setting"""
        async with self._create_session_factory() as session:
            yield session


async_session: AsyncSession = CreateSession(load_settings.db_url)
