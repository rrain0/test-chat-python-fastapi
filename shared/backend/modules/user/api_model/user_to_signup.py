from pydantic import BaseModel


class BackApiUserToSignup(BaseModel):
    username: str
    pwd: str
