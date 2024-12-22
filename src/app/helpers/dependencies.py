import contextlib

from fastapi import Request

from app.config import settings
from app.utils.logger import logger


def get_language_code(request: Request) -> str:
    """
    Dependency to extract and parse the language from the Accept-Language header.

    Args:
        request (Request): The HTTP request object to extract headers.

    Returns:
        str: The primary language code (e.g., "en-US").
    """
    language_code = settings.DEFAULT_LANGUAGE_HEADER_CODE
    accept_language = request.headers.get("accept-language", language_code)

    languages = []
    for lang in accept_language.split(","):
        parts = lang.strip().split(";")
        lang_code = parts[0].strip()
        q_value = 1.0  # Default q-value
        if len(parts) > 1 and parts[1].startswith("q="):
            with contextlib.suppress(ValueError):
                q_value = float(parts[1].split("=")[1])

        languages.append((lang_code, q_value))

    # Sort by q-value (highest first), then by the order of appearance
    languages.sort(key=lambda x: (-x[1], accept_language.index(x[0])))

    try:
        language_code = languages[0][0]
    except ValueError:
        logger.error(msg="The specified language could not be read. Defaulting to en.")

    return language_code
