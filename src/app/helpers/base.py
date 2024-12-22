from __future__ import annotations

import json

from pydantic import BaseModel, ConfigDict


class BaseModelConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias."""
        return json.loads(self.model_dump_json(by_alias=True, exclude_unset=True))

    def to_str(self) -> str:
        """Returns the string representation of the model using alias."""
        return str(self.model_dump_json(by_alias=True, exclude_unset=True))
