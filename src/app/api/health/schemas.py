from pydantic import BaseModel


class IndexResponse(BaseModel):
    message: str

    model_config = {"json_schema_extra": {"examples": [{"message": "Hello World!"}]}}


class HealthResponse(BaseModel):
    status: str

    model_config = {"json_schema_extra": {"examples": [{"status": "healthy"}]}}
