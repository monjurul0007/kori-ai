from enum import StrEnum
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Env(StrEnum):
    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """Service settings, read from `KORI_AI_*` environment variables."""

    model_config = SettingsConfigDict(env_prefix="KORI_AI_", env_file=".env", extra="ignore")

    env: Env = Env.DEVELOPMENT
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
