from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.utils.enums import Environment


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # ====================================
    # Database
    # ====================================

    DATABASE_USERNAME: str = "postgres"
    DATABASE_PASSWORD: str = "local"
    DATABASE_HOST: str = "localhost"
    DATABASE_NAME: str = "main"
    DATABASE_PORT: str = "5432"

    # ====================================
    # General
    # ====================================

    APP_NAME: str = "fastapi-template"
    ENVIRONMENT: str = Environment.dev
    LOG_LEVEL: str = "INFO"
    SSE_PING_INTERVAL: int = 2  # seconds

    # ====================================
    # OpenTelemetry
    # ====================================

    OTEL_EXPORTER_OTLP_ENDPOINT: str = "http://localhost:4318"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore is a bug in pyright https://github.com/pydantic/pydantic-settings/issues/201
