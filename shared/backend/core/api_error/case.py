from typing import Any
from pydantic import BaseModel


class ApiErrorCase(BaseModel):
    status_code: int
    error_code: str
    error_msg: str = ""
    error_detail: Any | None = None

    def eq_case(self, other: "ApiErrorCase") -> bool:
        return (
            self.status_code, self.error_code
        ) == (
            other.status_code, other.error_code
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ApiErrorCase): return NotImplemented
        return self.eq_case(other)
