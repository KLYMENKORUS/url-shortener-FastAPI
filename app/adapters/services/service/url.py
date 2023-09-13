from typing import Type, ClassVar
from dataclasses import dataclass

from fastapi import HTTPException, status

from ..database.core import DatabaseUOW
from ...utils.decorators import validator_url
from ...utils.keygen import CreateRandomKey
from app.api.common.schemas import URLBase, URLInfo, URLUpdate, URLCreate


@dataclass(slots=True)
class URLService:
    random_key: ClassVar[Type[CreateRandomKey]] = CreateRandomKey()

    @classmethod
    @validator_url
    async def create(
        cls, uow: Type[DatabaseUOW], query: URLBase
    ) -> URLInfo | None:
        async with uow:
            if not await uow.url_repo.select("target_url", query.target_url):
                query = query.model_dump(exclude_none=True)
                query.update(
                    key=cls.random_key(),
                    target_url=query.get("target_url"),
                )
                return await uow.url_repo.create(URLCreate(**query))
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Url {query.target_url} already exists",
                )
