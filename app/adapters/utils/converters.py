from starlette.datastructures import URL as StarletteURL

from app.api.common.schemas import URLInfo
from app.api.core.settings import load_settings
from app.adapters import URL


def convert_url_model_to_dto(url: URL) -> URLInfo:
    return URLInfo(
        id=url.id,
        target_url=url.target_url,
        is_active=url.is_active,
        clicks=url.clicks,
        short_url=url.key,
    )


def convert_key_to_short_url(url: URLInfo) -> URLInfo:
    base_url = StarletteURL(load_settings.base_url)

    return URLInfo(
        id=url.id,
        target_url=url.target_url,
        is_active=url.is_active,
        clicks=url.clicks,
        short_url=str(base_url.replace(path=url.short_url)),
    )
