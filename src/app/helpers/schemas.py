from __future__ import annotations

from pydantic import BaseModel, Field, StrictStr


class ApiError(BaseModel):
    """
    Error according to RFC-7807
    see: https://datatracker.ietf.org/doc/html/rfc7807
    """  # noqa: E501

    type: StrictStr = Field(
        description="A reference to the error type that identifies the problem type."
    )
    title: StrictStr = Field(
        description="A short, human-readable summary of the problem type."
    )
    detail: StrictStr | None = Field(
        default=None,
        description="A human-readable explanation specific to this occurrence of the problem.",
    )
    instance: StrictStr | None = Field(
        default=None,
        description="A reference that identifies the specific occurrence of the problem",
    )

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }
