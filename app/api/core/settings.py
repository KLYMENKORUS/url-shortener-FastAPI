from typing import Optional, Type
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    database_uri: str = (
        "postgresql+asyncpg://{}:{}@{}:{}/{}?async_fallback=True"
    )
    postgres_db: str
    postgres_host: Optional[str] = None
    postgres_port: Optional[int] = None
    postgres_user: Optional[str] = None
    postgres_password: Optional[str] = None

    @property
    def db_url(self) -> str:
        return self.database_uri.format(
            self.postgres_user,
            self.postgres_password,
            self.postgres_host,
            self.postgres_port,
            self.postgres_db,
        )


@lru_cache
def settings() -> Type[Settings]:
    return Settings()


load_settings = settings()
