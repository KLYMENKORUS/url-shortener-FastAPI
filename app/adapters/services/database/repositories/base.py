import abc
from typing import ClassVar, Type

from sqlalchemy.ext.asyncio import AsyncSession

from .crud import CRUDRepository, CRUDService, UOW, Model


class BaseRepository(abc.ABC):
    model: ClassVar[Type[Model]] = Model

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._crud = CRUDRepository(session, self.model)


class BaseService(abc.ABC):
    def __init__(self, uow: Type[UOW], repository: str) -> None:
        self._service = CRUDService(uow, repository)
