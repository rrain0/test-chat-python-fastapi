from uuid import UUID
from pydantic import BaseModel


class BackApiUser(BaseModel):
    id: UUID
    username: str
