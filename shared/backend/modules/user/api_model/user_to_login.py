from pydantic import BaseModel


class BackApiUserToLogin(BaseModel):
    login: str
    pwd: str
