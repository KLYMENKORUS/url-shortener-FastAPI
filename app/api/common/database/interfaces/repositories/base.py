import abc
from typing import Any, TypeVar, Optional, Protocol, Generic, Dict

from pydantic import BaseModel
from sqlalchemy import ColumnElement


T = TypeVar("T", bound=Any)
D = TypeVar("D", bound=Dict)
C = TypeVar("C", bound=ColumnElement)
Q = TypeVar("Q", bound=BaseModel, contravariant=True)
U = TypeVar("U", bound=BaseModel, contravariant=True)
TypeValue = TypeVar("TypeValue", contravariant=True)


class Repository(Protocol, Generic[D, T, Q, U, C]):
    @abc.abstractmethod
    async def create(self, query: Q) -> Optional[T]:
        raise NotImplementedError

    @abc.abstractmethod
    async def select(self, **kwargs: D) -> Optional[T]:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(self, *clauses: C, **query: U) -> T:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, *clauses: C) -> T:
        raise NotImplementedError


class Service(Protocol, Generic[TypeValue, T, Q]):
    @abc.abstractmethod
    async def create(self, query: Q) -> Optional[T]:
        raise NotImplementedError

    @abc.abstractmethod
    async def select(self, value: TypeValue) -> Optional[T]:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, value: TypeValue) -> T:
        raise NotImplementedError
