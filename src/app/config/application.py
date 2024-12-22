from app.config import settings
from app.utils.enums import Environment
from app.version import __version__

_DESCRIPTION = """WIP"""

# -------------- Docs Env-Settings --------------

_API_SETTINGS: dict = {
    Environment.dev: {
        "root_path": None,
        "openapi_url": "/openapi.json",
        "redoc_url": "/redoc",
    },
    Environment.sandbox: {
        "root_path": None,
        "openapi_url": None,
        "redoc_url": None,
    },
}

app_configs = {
    "title": "API checkmeineimmo.de",
    "description": _DESCRIPTION,
    "version": __version__,
    "contact": {
        "name": "Lorik Bajrami",
        "url": "https://checkmeineimmo.de",
    },
    "openapi_url": _API_SETTINGS.get(settings.ENVIRONMENT, {}).get("openapi_url"),
    "redoc_url": _API_SETTINGS.get(settings.ENVIRONMENT, {}).get("redoc_url"),
    "root_path": _API_SETTINGS.get(settings.ENVIRONMENT, {}).get("root_path"),
}

cors_config = {
    "allow_credentials": True,
    "allow_methods": ["GET", "POST", "PUT", "DELETE"],
    "allow_headers": ["*"],
    "allow_origins": ["*"],
}
