from pydantic import BaseModel

from shared.backend.modules.tg_user.api_model.tg_user import BackApiTgUser


class BackApiTgUserToSignup(BaseModel):
    username: str
    pwd: str
    tg_user: BackApiTgUser
