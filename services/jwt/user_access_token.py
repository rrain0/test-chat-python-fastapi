import datetime

from pydantic import BaseModel

from services.jwt.user_for_access_token import UserForAccessToken


class UserAccessToken(BaseModel):
    user: UserForAccessToken
    expires_at: datetime.datetime
