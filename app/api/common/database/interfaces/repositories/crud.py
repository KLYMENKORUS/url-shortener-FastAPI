import abc
from typing import (
    Any,
    Generic,
    Optional,
    Type,
    Sequence,
    TypeVar,
)
from sqlalchemy import ColumnElement

EntryType = TypeVar("EntryType")


class AbstractCRUDRepository(abc.ABC, Generic[EntryType]):
    def __init__(self, model: Type[EntryType]) -> None:
        self.model = model

    @abc.abstractmethod
    async def create(self, **kwargs: dict[str, Any]) -> Optional[EntryType]:
        raise NotImplementedError

    @abc.abstractmethod
    async def select(
        self, field: str, value: ColumnElement[bool]
    ) -> Optional[EntryType]:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(
        self, *clauses: ColumnElement[bool], **kwargs: dict[str, Any]
    ) -> Sequence[EntryType]:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(
        self, *clauses: ColumnElement[bool]
    ) -> Sequence[EntryType]:
        raise NotImplementedError
