import uuid

from pydantic import BaseModel


class UserForAccessToken(BaseModel):
    id: uuid.UUID
    login: str
