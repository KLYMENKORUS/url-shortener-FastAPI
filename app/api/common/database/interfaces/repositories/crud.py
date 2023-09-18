import abc
from typing import (
    Any,
    Generic,
    Optional,
    Type,
    TypeVar,
)
from sqlalchemy import ColumnElement

EntryType = TypeVar("EntryType")
EntryTypeUOW = TypeVar("EntryTypeUOW")


class AbstractCRUDRepository(abc.ABC, Generic[EntryType]):
    def __init__(self, model: Type[EntryType]) -> None:
        self.model = model

    @abc.abstractmethod
    async def create(self, **kwargs: dict[str, Any]) -> Optional[EntryType]:
        raise NotImplementedError

    @abc.abstractmethod
    async def select(self, **kwargs: dict[str, Any]) -> Optional[EntryType]:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(
        self, *clauses: ColumnElement[bool], **kwargs: dict[str, Any]
    ) -> EntryType:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, *clauses: ColumnElement[bool]) -> EntryType:
        raise NotImplementedError


class AbstractCRUDService(abc.ABC, Generic[EntryTypeUOW]):
    def __init__(self, uow: Type[EntryTypeUOW]) -> None:
        self.uow = uow

    @abc.abstractmethod
    async def create(
        self, field: str, value: Any, **kwargs: dict[str, Any]
    ) -> Optional[Any]:
        raise NotImplementedError

    @abc.abstractmethod
    async def select(self, **kwargs: dict[str, Any]) -> Optional[Any]:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(
        self,
        field: str,
        value: Any,
        *clauses: ColumnElement[bool],
        **kwargs: dict[str, Any]
    ) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, value: str) -> Any:
        raise NotImplementedError
