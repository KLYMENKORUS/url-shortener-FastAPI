import abc
from typing import Any, TypeVar, Optional, List, Protocol, Generic, Dict

from pydantic import BaseModel


T = TypeVar("T", bound=Any)
D = TypeVar("D", bound=Dict)
Q = TypeVar("Q", bound=BaseModel, contravariant=True)
U = TypeVar("U", bound=BaseModel, contravariant=True)
TypeValue = TypeVar("TypeValue", contravariant=True)


class Repository(Protocol, Generic[TypeValue, D, T, Q, U]):
    @abc.abstractmethod
    async def create(self, query: Q) -> Optional[T]:
        raise NotImplementedError

    @abc.abstractmethod
    async def select(self, **kwargs: D) -> Optional[T]:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(self, value: TypeValue, **query: U) -> T:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, value: TypeValue) -> List[T]:
        raise NotImplementedError
