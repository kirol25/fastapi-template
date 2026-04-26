from app.config import settings
from app.utils.enums import Environment
from app.version import __version__

_DESCRIPTION = """A production-ready FastAPI template with PostgreSQL, SQLAlchemy, Alembic, OpenTelemetry, and more."""

_is_dev = Environment.dev == settings.ENVIRONMENT

app_configs = {
    "title": "FastAPI Template",
    "description": _DESCRIPTION,
    "version": __version__,
    "openapi_url": "/openapi.json" if _is_dev else None,
    "redoc_url": "/redoc" if _is_dev else None,
}

cors_config = {
    "allow_credentials": True,
    "allow_methods": ["GET", "POST", "PUT", "DELETE"],
    "allow_headers": ["*"],
    "allow_origins": ["*"],
}
