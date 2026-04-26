from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from app.config import settings
from app.config.database import engine
from app.utils.enums import Environment


def init_opentelemetry(app: FastAPI) -> None:
    """
    Initialize OpenTelemetry with FastAPI and set up span processors.
    This function should be called once in the application startup.

    Args:
        app (FastAPI): The FastAPI application instance for which OpenTelemetry will be initialized.
    """

    provider = TracerProvider(resource=_get_resources())
    trace.set_tracer_provider(provider)

    otlp_exporter = OTLPSpanExporter(endpoint=settings.OTEL_EXPORTER_OTLP_ENDPOINT)
    span_processor = BatchSpanProcessor(otlp_exporter)

    provider.add_span_processor(span_processor)

    # --- Instrumentor ---
    FastAPIInstrumentor().instrument_app(
        app,
        tracer_provider=provider,
        excluded_urls="/monitoring/*, ^/$",
    )
    SQLAlchemyInstrumentor().instrument(
        enable_commenter=True, commenter_options={}, engine=engine
    )


def _get_resources() -> Resource:
    """
    Retrieves the resources for the OpenTelemetry TracerProvider,
    ensuring the environment specified in the settings is valid.

    Returns:
        Resource: An OpenTelemetry Resource object with the appropriate
        service name attribute, where `service.name` is set to
        "<environment>-<project_name>".

    Raises:
        Exception: If the environment does not exist.
    """
    if settings.ENVIRONMENT not in Environment.list_values():
        raise Exception(
            f"The provided Environment {settings.ENVIRONMENT} is not known!"
        )
    return Resource(
        attributes={"service.name": f"{settings.ENVIRONMENT}-{settings.APP_NAME}"}
    )
