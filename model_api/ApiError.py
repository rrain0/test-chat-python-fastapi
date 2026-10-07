from pydantic import BaseModel


class ApiError(BaseModel):
    error_code: str
    description: str