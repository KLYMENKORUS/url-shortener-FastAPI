from app.api.common.schemas import URLInfo
from app.adapters import URL


def convert_url_model_to_dto(url: URL) -> URLInfo:
    return URLInfo(
        target_url=url.target_url,
        is_active=url.is_active,
        clicks=url.clicks,
        short_url=url.key,
    )
