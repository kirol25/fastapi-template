from __future__ import annotations

import json

from pydantic import BaseModel, ConfigDict


class BaseModelConfig(BaseModel):
    """Base Pydantic model with ORM mode enabled."""

    model_config = ConfigDict(from_attributes=True)

    def to_json(self) -> dict:
        """Return the model as a JSON-compatible dict using aliases."""
        return json.loads(self.model_dump_json(by_alias=True, exclude_unset=True))

    def to_str(self) -> str:
        """Returns the string representation of the model using alias."""
        return str(self.model_dump_json(by_alias=True, exclude_unset=True))
