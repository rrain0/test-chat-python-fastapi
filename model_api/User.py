import uuid
from pydantic import BaseModel


class User(BaseModel):
    id: uuid.UUID
    login: str
