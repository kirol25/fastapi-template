import asyncio
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.utils.logger import logger

_SKIP_PATHS = {"/", "/monitoring/health", "/monitoring/metrics"}


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log every request with method, path, status, and duration."""

    async def dispatch(self, request: Request, call_next) -> Response:
        if request.url.path in _SKIP_PATHS:
            return await call_next(request)

        start = time.perf_counter()
        status_code = 500

        try:
            response = await call_next(request)
            status_code = response.status_code
        except asyncio.CancelledError:
            raise
        finally:
            duration_ms = round((time.perf_counter() - start) * 1000, 1)
            log = logger.bind(
                method=request.method,
                path=request.url.path,
                status_code=status_code,
                duration_ms=duration_ms,
                client_ip=self._get_client_ip(request),
            )
            if status_code >= 500:
                log.error("request_error")
            elif status_code >= 400:
                log.warning("request_warning")
            else:
                log.info("request")

        return response

    @staticmethod
    def _get_client_ip(request: Request) -> str:
        """Extract client IP from X-Forwarded-For or connection info."""
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return str(request.client.host) if request.client else "unknown"
