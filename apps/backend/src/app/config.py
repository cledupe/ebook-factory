from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    log_level: str = "INFO"

    database_url: str = "sqlite+aiosqlite:///./test.db"
    sync_database_url: str = "sqlite:///./test.db"
    redis_url: str = "redis://localhost:6379/0"
    storage_endpoint: str = "http://localhost:9000"
    storage_access_key: str = "ebook"
    storage_secret_key: str = "ebook-secret"
    storage_bucket: str = "ebook-factory"
    storage_access_key: str = "ebook"
    storage_secret_key: str = "ebook-secret"
    storage_bucket: str = "ebook-factory"


@lru_cache
def get_settings() -> Settings:
    return Settings()
