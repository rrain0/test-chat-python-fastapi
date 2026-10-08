from typing import Any

from pydantic import BaseModel


class ApiError(BaseModel):
    error_code: str
    msg: str = ""
    detail: Any | None = None
