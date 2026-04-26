from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.api import router
from app.api.health.schemas import IndexResponse
from app.config.application import app_configs, cors_config
from app.config.limiter import limiter
from app.config.middlewares import RequestLoggingMiddleware
from app.utils.logger import configure_logging
from app.utils.opentelemetry import init_opentelemetry

configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown logic for the application."""
    yield


app = FastAPI(**app_configs, lifespan=lifespan)

# Rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Middleware (order matters: last added = first executed)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(CORSMiddleware, **cors_config)

# Routes
app.include_router(router)

# Prometheus metrics
Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    excluded_handlers=["/monitoring", "/openapi.json", "/docs", "/redoc"],
).instrument(app).expose(app, endpoint="/monitoring/metrics", tags=["Monitoring"])

# OpenTelemetry
init_opentelemetry(app)


@app.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=IndexResponse,
    description="Root endpoint providing a welcome message.",
    tags=["Root"],
)
async def index() -> IndexResponse:
    """Root endpoint of the API."""
    return IndexResponse(message="Hello World!")


def main() -> None:
    """Run the application using Uvicorn."""
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True, log_config=None)


if __name__ == "__main__":
    main()
