from pydantic import BaseModel


class BackApiTgBotUserToLogin(BaseModel):
    login: str
    pwd: str
