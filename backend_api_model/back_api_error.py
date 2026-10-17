from typing import Any

from pydantic import BaseModel


class BackApiError(BaseModel):
    error_code: str
    msg: str = ""
    detail: Any | None = None
