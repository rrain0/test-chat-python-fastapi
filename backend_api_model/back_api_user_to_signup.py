from pydantic import BaseModel


class BackApiUserToSignup(BaseModel):
    login: str
    pwd: str
