from pydantic import BaseModel, ConfigDict, field_validator
from typing import Any

class ApiResponse(BaseModel):
    model_config = ConfigDict(extra='allow')

    @classmethod
    def from_api(cls, data: dict, status_code: int) -> "ApiResponse":
        obj = cls.model_validate(data)
        obj.__dict__["_status_code"] = status_code
        return obj

    @property
    def status_code(self) -> int:
        return getattr(self, "_status_code", 0)