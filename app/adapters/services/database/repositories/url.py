from typing import ClassVar, List, Type, Any

from sqlalchemy import ColumnElement

from app.api.common.database.interfaces.repositories import Repository
from app.api.common.schemas import URLInfo, URLCreate, URLUpdate
from app.adapters import URL
from app.adapters.utils.converters import convert_url_model_to_dto
from .base import BaseRepository


class URLRepository(
    BaseRepository,
    Repository[
        str,
        dict[str, Any],
        URLInfo,
        URLCreate,
        dict[str, URL],
        ColumnElement[bool],
    ],
):
    model: ClassVar[Type[URL]] = URL

    async def create(self, query: URLCreate) -> URLInfo | None:
        result = await self._crud.create(**query.model_dump(exclude_none=True))

        return convert_url_model_to_dto(result)

    async def select(self, **kwargs: dict[str, Any]) -> URLInfo | None:
        result = await self._crud.select(**kwargs)

        if result is None:
            return None

        return convert_url_model_to_dto(result)

    async def update(
        self, *clauses: ColumnElement[bool], **query: dict[str, URL]
    ) -> URLInfo:
        return await self._crud.update(*clauses, **query)

    async def delete(self, value: str) -> List[URLInfo]:
        return await super().delete(value)
