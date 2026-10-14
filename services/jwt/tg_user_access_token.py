import datetime

from pydantic import BaseModel

from services.jwt.tg_user_for_access_token import TgUserForAccessToken
from services.jwt.user_for_access_token import UserForAccessToken


class TgUserAccessToken(BaseModel):
    user: UserForAccessToken
    tg_user: TgUserForAccessToken
    expires_at: datetime.datetime
