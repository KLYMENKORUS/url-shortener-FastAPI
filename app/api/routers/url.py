from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.api.common.schemas import URLBase, URLInfo
from app.adapters.dependencies import UOWDepends
from app.adapters.services.service import URLService


router = APIRouter(tags=["url"])


@router.post(
    "/add",
    summary="adding a new URL for shortening",
    response_model=URLInfo,
)
async def add_url(url: URLBase, uow: UOWDepends) -> URLInfo:
    return await URLService(uow).create(url)


@router.get(
    "/select/{url_key}",
    summary="Getting a URL information",
    response_model=URLInfo,
)
async def select(url_key: str, uow: UOWDepends):
    return await URLService(uow).select(url_key)


@router.get(
    "/{url_key}",
    summary="forward a shortened URL",
    response_class=RedirectResponse,
)
async def forward_to_target_url(
    url_key: str, uow: UOWDepends
) -> RedirectResponse:
    return await URLService(uow).forward_to_target_url(url_key)
