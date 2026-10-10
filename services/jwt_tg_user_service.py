import datetime
import jwt
from pydantic import BaseModel

from env import TG_USER_ACCESS_TOKEN_LIFETIME, TG_USER_ACCESS_TOKEN_SECRET
from utils.datetimes import parse_duration, now



class TgUserAccessToken(BaseModel):
    user_id: int
    user_username: str | None
    user_first_name: str
    user_last_name: str | None
    expires_at: datetime.datetime



def create_tg_user_access_token(
        user_id: int,
        user_username: str | None,
        user_first_name: str,
        user_last_name: str | None,
        created_at: datetime.datetime,
) -> str:
    lifetime = datetime.timedelta(milliseconds=parse_duration(TG_USER_ACCESS_TOKEN_LIFETIME))
    expires_at = created_at + lifetime

    data = {
        "type": "tg_user",
        "exp": int(expires_at.timestamp()),
        "sub": str(user_id),
        "user_username": user_username,
        "user_first_name": user_first_name,
        "user_last_name": user_last_name,
    }

    token = jwt.encode(
        data,
        TG_USER_ACCESS_TOKEN_SECRET,
        algorithm='HS256'
    )

    return token



def decode_tg_user_access_token(token: str) -> TgUserAccessToken:
    payload = jwt.decode(token, TG_USER_ACCESS_TOKEN_SECRET, algorithms=['HS256'])

    type = payload['type']
    if type != 'tg_user':
        raise jwt.InvalidTokenError

    expires_at_ts = int(payload['exp'])
    expired = int(now().timestamp()) > expires_at_ts
    if expired:
        raise jwt.InvalidTokenError
    expires_at = datetime.datetime.fromtimestamp(expires_at_ts)

    id_str = payload['sub']
    if not id_str:
        raise jwt.InvalidTokenError
    id_int = int(id_str)

    user_username = payload['user_username']

    user_first_name = payload['user_first_name']

    user_last_name = payload['user_last_name']

    return TgUserAccessToken(
        user_id=id_int,
        user_username=user_username,
        user_first_name=user_first_name,
        user_last_name=user_last_name,
        expires_at=expires_at,
    )