import uuid
from pydantic import BaseModel


class BackApiUser(BaseModel):
    id: uuid.UUID
    login: str

