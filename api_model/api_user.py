import uuid
from pydantic import BaseModel


class ApiUser(BaseModel):
    id: uuid.UUID
    login: str



