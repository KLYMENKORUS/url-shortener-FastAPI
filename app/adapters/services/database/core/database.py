from typing import Any, Type

from .unit_of_work import UnitOfWork


class DatabaseUOW:
    def __init__(self) -> None:
        self._uow = UnitOfWork()

    async def __aenter__(self) -> Type["DatabaseUOW"]:
        await self._uow.__aenter__()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self._uow.__aexit__(*args)
        return

    @property
    def url_repo(self) -> Type["URLRepository"]:
        return self._uow._mediator.urlrepository
