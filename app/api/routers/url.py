from fastapi import APIRouter

from app.api.common.schemas import URLBase, URLInfo
from app.adapters.dependencies import UOWDepends
from app.adapters.services.service import URLService


router = APIRouter(prefix="/url", tags=["url"])


@router.post(
    "/add", summary="adding a new URL for shortening", response_model=URLInfo
)
async def add_url(url: URLBase, uow: UOWDepends) -> URLInfo:
    return await URLService.create(uow, url)
