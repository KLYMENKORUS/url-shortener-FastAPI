from typing import (
    Any,
    TypeVar,
    Type,
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

    async def delete(self, *clauses: ColumnElement[bool]) -> Model:
        stmt = delete(self.model).where(*clauses).returning(self.model)
        return (await self._session.execute(stmt)).scalars().first()


class CRUDService(AbstractCRUDService[UOW]):
    def __init__(self, uow: Type[UOW], repository: str) -> None:
        super().__init__(uow)
        self._repository_name = repository

    async def create(
        self, field: str, value: Any, kwargs: Type[ModelBase]
    ) -> Any | None:
        async with self.uow:
            self._repository = getattr(self.uow, self._repository_name)
            if not await self._repository.select(**{field: value}):
                return await self._repository.create(kwargs)

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The {value} already exists",
            )

    async def select(self, **kwargs: dict[str, Any]) -> Any | None:
        async with self.uow:
            self._repository = getattr(self.uow, self._repository_name)
            data = await self._repository.select(**kwargs)

            if data is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="The does not exist",
                )

            return data

    async def update(
        self,
        field: str,
        value: Any,
        *clauses: ColumnElement[bool],
        **kwargs: dict[str, Any],
    ) -> Any:
        async with self.uow:
            self._repository = getattr(self.uow, self._repository_name)
            if not await self._repository.select(**{field: value}):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"The key {value} does not exist",
                )

            return await self._repository.update(*clauses, **kwargs)

    async def delete(
        self, field: str, value: Any, *clauses: ColumnElement[bool]
    ) -> Any:
        async with self.uow:
            self._repository = getattr(self.uow, self._repository_name)
            if not await self._repository.select(**{field: value}):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"The key {value} does not exist",
                )

            return await self._repository.delete(*clauses)
