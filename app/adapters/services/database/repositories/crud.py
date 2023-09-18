from typing import (
    Any,
    TypeVar,
    Type,
    Sequence,
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    select,
    insert,
    update,
    delete,
    ColumnElement,
)
from fastapi import HTTPException, status
from pydantic import BaseModel

from app.api.common.database.interfaces.repositories import (
    AbstractCRUDRepository,
    AbstractCRUDService,
)
from app.adapters import Base


Model = TypeVar("Model", bound=Base)
UOW = TypeVar("UOW")
ModelBase = TypeVar("ModelBase", bound=BaseModel)


class CRUDRepository(AbstractCRUDRepository[Model]):
    def __init__(self, session: AsyncSession, model: Type[Model]) -> None:
        super().__init__(model)
        self._session = session

    async def create(self, **kwargs: dict[str, Any]) -> Model | None:
        stmt = insert(self.model).values(**kwargs).returning(self.model)
        return (await self._session.execute(stmt)).scalars().first()

    async def select(self, **kwargs: dict[str, Any]) -> Model | None:
        stmt = select(self.model).filter_by(**kwargs)
        return (await self._session.execute(stmt)).scalars().first()

    async def update(
        self, *clauses: ColumnElement[bool], **kwargs: dict[str, Any]
    ) -> Model:
        stmt = (
            update(self.model)
            .where(*clauses)
            .values(**kwargs)
            .returning(self.model)
        )

        return (await self._session.execute(stmt)).scalars().first()

    async def delete(self, *clauses: ColumnElement[bool]) -> Sequence[Model]:
        stmt = delete(self.model).where(*clauses).returning(self.model)
        return (await self._session.execute(stmt)).scalars().all()


class CRUDService(AbstractCRUDService[UOW]):
    def __init__(self, uow: Type[UOW], repository: str) -> None:
        super().__init__(uow)
        self._repository = repository

    async def create(
        self, field: str, value: Any, kwargs: Type[ModelBase]
    ) -> Any | None:
        async with self.uow:
            self._repository = getattr(self.uow, self._repository)
            if not await self._repository.select(**{field: value}):
                return await self._repository.create(kwargs)
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"The {value} already exists",
                )

    async def select(self, value: str) -> Any | None:
        return await super().select(value)

    async def update(self, **kwargs: dict[str, Any]) -> Any:
        return await super().update(**kwargs)

    async def delete(self, value: str) -> Any:
        return await super().delete(value)
