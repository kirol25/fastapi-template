from pydantic import BaseModel


class IndexResponse(BaseModel):
    """Response for the index endpoint."""

    message: str

    model_config = {"json_schema_extra": {"examples": [{"message": "Hello World!"}]}}


class HealthResponse(BaseModel):
    """Response for the health check endpoint."""

    status: str

    model_config = {"json_schema_extra": {"examples": [{"status": "healthy"}]}}
