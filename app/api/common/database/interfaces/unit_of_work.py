from __future__ import annotations

import abc
from typing import Optional, Type
from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

from app.adapters.services.database.core import async_session

from .mediator import build_mediator, Mediator


class AbstractUnitOfWork(abc.ABC):
    def __init__(self) -> None:
        self._session_factory = async_session
        self._session_transaction: Optional[AsyncSessionTransaction] = None

    async def __aenter__(self) -> Type["AbstractUnitOfWork"]:
        self._session: AsyncSession = await self._session_factory()
        await self._create_transaction()

        self._mediator: Type[Mediator] = build_mediator(self._session)

        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        if self._session_transaction:
            if exc_type:
                await self._session.rollback()
            else:
                await self._session.commit()

        await self._session.close()

    async def _create_transaction(self) -> None:
        if not self._session.in_transaction() and self._session.is_active:
            self._session_transaction = await self._session.begin()

    @abc.abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
