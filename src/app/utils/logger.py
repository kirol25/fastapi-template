"""
This module configures logging for the application using the `logging` and `structlog` libraries.
It sets up a console handler with formatting suitable for development environments.
The log level can be adjusted via an environment variable.
Additionally, it loads environment variables from a `.env` file at the start.
"""

import json
import logging
from datetime import UTC, datetime
from logging import Formatter

from asgi_correlation_id import CorrelationIdFilter
from opentelemetry import trace

from app.config import settings
from app.utils.enums import Environment

DATE_FORMAT_TIMEZONE = "%Y-%m-%dT%H:%M:%S.%fZ"
EXCLUDED_KEYS = {
    "request_id",
    "correlation_id",
    "req",
    "res",
    "level",
    "message",
    "timestamp",
    "exc_info",
    "exc_text",
    "filename",
    "pathname",
    "funcName",
    "args",
    "levelno",
    "module",
    "stack_info",
    "lineno",
    "created",
    "msecs",
    "relativeCreated",
    "threadName",
    "processName",
    "process",
    "thread",
    # FastAPI
    "color_message",
    "name",
    "msg",
}


class JsonFormatter(Formatter):
    """
    Custom log formatter that outputs logs in JSON format.

    This formatter serializes log records into JSON, including request and response information if available.
    """

    def __init__(self) -> None:
        super().__init__()

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats a log record into a JSON string.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The JSON-formatted log record as a string.
        """
        json_record = {
            "level": record.levelname,
            "timestamp": datetime.now(tz=UTC).strftime(DATE_FORMAT_TIMEZONE),
            "message": record.getMessage(),
        }

        current_span = trace.get_current_span()
        if current_span and current_span.get_span_context().trace_id != 0:
            json_record["trace_id"] = format(
                current_span.get_span_context().trace_id, "032x"
            )
            json_record["span_id"] = format(
                current_span.get_span_context().span_id, "016x"
            )

        if "correlation_id" in record.__dict__ and record.__dict__["correlation_id"]:
            json_record["request_id"] = record.__dict__["correlation_id"]

        if "req" in record.__dict__:
            json_record["request"] = record.__dict__["req"]

        if "res" in record.__dict__:
            json_record["response"] = record.__dict__["res"]

        # Handle additional custom fields (e.g., new_user_request)
        for key, value in record.__dict__.items():
            if key not in EXCLUDED_KEYS:
                json_record[key] = self._serialize_value(value)

        if record.levelno == logging.ERROR and record.exc_info:
            json_record["err"] = self.formatException(record.exc_info)
        return json.dumps(json_record)

    @staticmethod
    def _serialize_value(value: object) -> str:
        """
        Ensures that the value is JSON serializable.

        Args:
            value: The value to serialize.

        Returns:
            str: The serialized value as a string.
        """
        if not isinstance(value, str):
            return str(value)
        try:
            json.dumps(value)
            return value
        except TypeError:
            return str(value)


logger = logging.getLogger(settings.APP_NAME)
handler = logging.StreamHandler()
logger.setLevel(settings.LOG_LEVEL)
logger.handlers = [handler]
handler.addFilter(CorrelationIdFilter(uuid_length=32))


logging.getLogger("httpx").setLevel(
    logging.WARNING
)  # https://github.com/langchain-ai/langchain/issues/14065

if Environment.dev == settings.ENVIRONMENT:
    # Use default logger configuration
    logging.basicConfig(level=settings.LOG_LEVEL)
else:
    handler.setFormatter(JsonFormatter())

    # Disable the default Uvicorn access logger
    logging.getLogger("uvicorn.access").disabled = True
