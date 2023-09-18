__all__ = (
    "BaseRepository",
    "BaseService",
    "URLRepository",
)

from .base import BaseRepository, BaseService
from .url import URLRepository

REPOSITORIES = (URLRepository,)
