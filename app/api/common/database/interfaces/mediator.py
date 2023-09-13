from typing import Any, Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.services.database.repositories import (
    BaseRepository,
    REPOSITORIES,
)


class Mediator:
    def __init__(self) -> None:
        self._repositories: dict[str, BaseRepository] = {}

    def add(self, repository: BaseRepository) -> None:
        self._repositories[type(repository).__name__.lower()] = repository

    def __getattr__(self, key: str) -> Any:
        if key in self._repositories:
            return self._repositories[key]

        raise AttributeError(
            f"{type(self).__name__} object has no attribute '{key}'"
        )

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name != "_repositories":
            self._repositories[__name] = __value
        else:
            super().__setattr__(__name, __value)


def build_mediator(session: AsyncSession) -> Type[Mediator]:
    mediator = Mediator()

    for repository in REPOSITORIES:
        mediator.add(repository(session))

    return mediator
