import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.utils.logger import logger


class LogMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log HTTP requests and responses with a unique request ID.

    This middleware generates a unique request ID for each request and logs the incoming request details and response status.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Processes an incoming request, logs its details along with the response status, and then returns the response.

        Args:
            request (Request): The incoming HTTP request.
            call_next (Callable): A function to call the next middleware or endpoint.

        Returns:
            Response: The HTTP response generated after processing the request.
        """
        response = await call_next(request)
        client_ip_address = self._get_client_ip_address(request)

        log_level = (
            logging.DEBUG
            if request.url.path in ("/", "/health", "/metrics")
            else logging.INFO
        )
        logger.log(
            log_level,
            "Incoming request",
            extra={
                "request": {
                    "ip_address": client_ip_address,
                    "method": request.method,
                    "url": str(request.url),
                },
                "response": {
                    "status_code": response.status_code,
                },
            },
        )
        return response

    @staticmethod
    def _get_client_ip_address(request: Request) -> str:
        """
        Retrieves the client's IP address from the given request.

        Args:
            request: The request object containing HTTP headers and connection information.

        Returns:
            str: The client's IP address as a string.
        """
        client_ip = request.headers.get("X-Forwarded-For")
        if client_ip:
            # X-Forwarded-For could have multiple IPs, the first one is the original client
            client_ip = client_ip.split(",")[0].strip()
        else:
            # Fallback to request.client.host if 'X-Forwarded-For' is not set
            client_ip = str(request.client.host) if request.client else "unknown"

        return client_ip
