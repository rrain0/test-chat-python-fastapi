from typing import Any

from pydantic import BaseModel


class BackApiError(BaseModel):
    error_code: str
    error_msg: str = ""
    error_detail: Any | None = None
