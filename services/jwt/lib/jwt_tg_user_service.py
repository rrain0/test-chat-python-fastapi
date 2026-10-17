import datetime
import uuid

import jwt

from env import TG_USER_ACCESS_TOKEN_LIFETIME, TG_USER_ACCESS_TOKEN_SECRET
from services.jwt.model.tg_user_access_token import TgUserAccessToken
from services.jwt.model.tg_user_for_access_token import TgUserForAccessToken
from services.jwt.model.user_for_access_token import UserForAccessToken
from utils.datetimes import parse_duration, now



def create_tg_user_access_token(
        user: UserForAccessToken,
        tg_user: TgUserForAccessToken,
        created_at: datetime.datetime,
) -> str:
    lifetime = datetime.timedelta(milliseconds=parse_duration(TG_USER_ACCESS_TOKEN_LIFETIME))
    expires_at = created_at + lifetime

    data = {
        "type": "tg_user",
        "exp": int(expires_at.timestamp()),
        "sub": str(tg_user.id),
        "tg_user_username": tg_user.username,
        "tg_user_first_name": tg_user.first_name,
        "tg_user_last_name": tg_user.last_name,
        "user_id": str(user.id),
        "user_login": user.login,
    }

    token = jwt.encode(
        payload=data,
        key=TG_USER_ACCESS_TOKEN_SECRET,
        algorithm='HS256'
    )

    return token



def decode_tg_user_access_token(token: str) -> TgUserAccessToken:
    payload = jwt.decode(
        jwt=token,
        key=TG_USER_ACCESS_TOKEN_SECRET,
        algorithms=['HS256']
    )

    type = payload['type']
    if type != 'tg_user':
        raise jwt.InvalidTokenError

    expires_at_ts = int(payload['exp'])
    expired = int(now().timestamp()) > expires_at_ts
    if expired:
        raise jwt.InvalidTokenError
    expires_at = datetime.datetime.fromtimestamp(expires_at_ts)

    tg_user_id_str = payload['sub']
    if not tg_user_id_str:
        raise jwt.InvalidTokenError
    tg_user_id = int(tg_user_id_str)

    tg_user_username = payload['tg_user_username']

    tg_user_first_name = payload['tg_user_first_name']

    tg_user_last_name = payload['tg_user_last_name']

    user_id_str = payload['user_id']
    if not user_id_str:
        raise jwt.InvalidTokenError
    user_id = uuid.UUID(user_id_str)

    user_login = payload['user_login']
    if not isinstance(user_login, str):
        raise jwt.InvalidTokenError

    return TgUserAccessToken(
        user=UserForAccessToken(
            id=user_id,
            login=user_login
        ),
        tg_user=TgUserForAccessToken(
            id=tg_user_id,
            username=tg_user_username,
            first_name=tg_user_first_name,
            last_name=tg_user_last_name,
        ),
        expires_at=expires_at,
    )