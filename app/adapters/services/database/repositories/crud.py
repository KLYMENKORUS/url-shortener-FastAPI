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

from app.api.common.database.interfaces.repositories import (
    AbstractCRUDRepository,
)
from app.adapters import Base


Model = TypeVar("Model", bound=Base)


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
    ) -> Sequence[Model]:
        stmt = (
            update(self.model)
            .where(*clauses)
            .values(**kwargs)
            .returning(self.model)
        )

        return (await self._session.execute(stmt)).scalars().all()

    async def delete(self, *clauses: ColumnElement[bool]) -> Sequence[Model]:
        stmt = delete(self.model).where(*clauses).returning(self.model)
        return (await self._session.execute(stmt)).scalars().all()
