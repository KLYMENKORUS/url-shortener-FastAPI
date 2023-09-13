__all__ = (
    "BaseRepository",
    "URLRepository",
)

from .base import BaseRepository
from .url import URLRepository

REPOSITORIES = (URLRepository,)
