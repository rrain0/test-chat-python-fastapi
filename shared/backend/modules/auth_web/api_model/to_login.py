from pydantic import BaseModel


class BackApiWebUserToLogin(BaseModel):
    login: str
    pwd: str
