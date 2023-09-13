from sqlalchemy.exc import SQLAlchemyError

from app.adapters.utils.exceptions import CommitError, RollbackError
from app.api.common.database import AbstractUnitOfWork


class UnitOfWork(AbstractUnitOfWork):
    async def commit(self) -> None:
        try:
            await self._session.commit()
        except SQLAlchemyError as err:
            raise CommitError from err

    async def rollback(self) -> None:
        try:
            await self._session.rollback()
        except SQLAlchemyError as err:
            raise RollbackError from err
