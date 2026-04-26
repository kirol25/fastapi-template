import uuid

from pydantic import Field

from app.helpers.base import BaseModelConfig


class UserResponse(BaseModelConfig):
    """Response schema for user data."""

    id: uuid.UUID = Field(..., description="Unique identifier for the user.")
    username: str = Field(..., description="Username of the user.")
    name: str | None = Field(None, description="Full name of the user. Optional.")
