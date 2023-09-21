from typing import Type

from ..database.core import DatabaseUOW
from ...utils.decorators import validator_url
from ...utils.keygen import CreateRandomKey
from ...utils.converters import convert_key_to_short_url
from ..database.repositories import BaseService
from app.api.common.schemas import URLBase, URLInfo, URLCreate
from app.api.common.database.interfaces.repositories import Service
from app.adapters import URL


class URLService(BaseService, Service[str, URLInfo, URLBase]):
    def __init__(self, uow: Type[DatabaseUOW]) -> None:
        super(URLService, self).__init__(uow, "url_repo")
        self.random_key: Type[CreateRandomKey] = CreateRandomKey()

    @validator_url
    async def create(self, query: URLBase) -> URLInfo | None:
        query = query.model_dump(exclude_none=True)
        query.update(
            key=self.random_key(),
            target_url=query.get("target_url"),
        )
        result = await self._service.create(
            "target_url",
            query.get("target_url"),
            URLCreate(**query),
        )
        return convert_key_to_short_url(result)

    async def select(self, value: str) -> URLInfo | None:
        result = await self._service.select(key=value, is_active=True)
        return convert_key_to_short_url(result)

    async def delete(self, value: str) -> URLInfo:
        return await self._service.delete(
            "key", value, URL.key == value, URL.is_active == True
        )

    async def forward_to_target_url(self, key: str) -> str | None:
        forward_url = await self._service.select(key=key, is_active=True)

        return (
            await self._service.update(
                "key",
                key,
                URL.key == forward_url.short_url,
                URL.is_active == True,
                clicks=forward_url.clicks + 1,
            )
        ).target_url
