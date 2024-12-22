import uvicorn
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.api import router
from app.api.health.schemas import IndexResponse
from app.config.application import app_configs, cors_config
from app.config.middlewares import LogMiddleware
from app.utils.opentelemetry import init_opentelemetry

# -------------- Start app --------------

app = FastAPI(**app_configs)

# -------------- Setup Middlewares  --------------

app.add_middleware(LogMiddleware)

# -------------- Setup CORS --------------

app.add_middleware(CORSMiddleware, **cors_config)

# -------------- API-Router --------------

app.include_router(router)

# -------------- Expose /metrics endpoint  --------------

Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    excluded_handlers=["/monitoring", "/openapi.json", "/docs", "/redoc"],
).instrument(app).expose(app, endpoint="/monitoring/metrics", tags=["Monitoring"])

# -------------- Initialize OpenTelemetry --------------

init_opentelemetry(app)


@app.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=IndexResponse,
    description="Root endpoint providing a welcome message.",
    tags=["Root"],
)
async def index() -> IndexResponse:
    """
    Root endpoint of the API.

    This endpoint provides a welcome message to users accessing the APIs root path.
    It serves as a simple introduction or entry point to the service.

    Returns:
        dict: A dictionary containing a welcome message.
    """
    return IndexResponse(message="Hello World!")


def main() -> None:
    """
    The main function to run the application using Uvicorn.
    """

    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True, log_config=None)


if __name__ == "__main__":
    main()
