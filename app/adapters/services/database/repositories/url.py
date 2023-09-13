from typing import ClassVar, List, Type

from app.api.common.database.interfaces.repositories import Repository
from app.api.common.schemas import URLInfo, URLCreate, URLUpdate
from app.adapters import URL
from app.adapters.utils.converters import convert_url_model_to_dto
from app.api.common.schemas.url import URLUpdate
from .base import BaseRepository


class URLRepository(
    BaseRepository, Repository[str, str, URLInfo, URLCreate, URLUpdate]
):
    model: ClassVar[Type[URL]] = URL

    async def create(self, query: URLCreate) -> URLInfo | None:
        result = await self._crud.create(**query.model_dump(exclude_none=True))

        return convert_url_model_to_dto(result)

    async def select(self, field: str, value: str) -> URLInfo | None:
        result = await self._crud.select(field, value)

        if result is None:
            return None

        return convert_url_model_to_dto(result)

    async def update(
        self, value: str, query: URLUpdate, exclude_none: bool = True
    ) -> List[URLInfo]:
        return await super().update(value, query, exclude_none)

    async def delete(self, value: str) -> List[URLInfo]:
        return await super().delete(value)
