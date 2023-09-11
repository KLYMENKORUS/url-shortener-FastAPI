import abc
from typing import Any, TypeVar, Optional, List, Protocol, Generic

from pydantic import BaseModel


T = TypeVar("T", bound=Any)
Q = TypeVar("Q", bound=BaseModel, contravariant=True)
U = TypeVar("U", bound=BaseModel, contravariant=True)
TypeValue = TypeVar("TypeValue", contravariant=True)


class BaseRepository(Protocol, Generic[TypeValue, T, Q, U]):
    @abc.abstractmethod
    async def create(self, query: Q) -> Optional[T]:
        raise NotImplementedError

    @abc.abstractmethod
    async def select(self, value: TypeValue) -> Optional[T]:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(
        self, value: TypeValue, query: U, exclude_none: bool = True
    ) -> List[T]:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, value: TypeValue) -> List[T]:
        raise NotImplementedError