from pydantic import BaseModel

from backend_api_model.back_api_tg_user import BackApiTgUser


class BackApiTgUserLogin(BaseModel):
    login: str
    pwd: str
    tg_user: BackApiTgUser
