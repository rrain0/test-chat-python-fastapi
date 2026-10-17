import datetime
import uuid
import jwt

from env import USER_ACCESS_TOKEN_LIFETIME, USER_ACCESS_TOKEN_SECRET
from services.jwt.model.user_access_token import UserAccessToken
from services.jwt.model.user_for_access_token import UserForAccessToken
from utils.datetimes import parse_duration, now


def create_user_access_token(
        user: UserForAccessToken,
        created_at: datetime.datetime,
) -> str:
    lifetime = datetime.timedelta(milliseconds=parse_duration(USER_ACCESS_TOKEN_LIFETIME))
    expires_at = created_at + lifetime

    data = {
        "type": "user",
        "exp": int(expires_at.timestamp()),
        "sub": str(user.id),
        "login": user.login,
    }

    token = jwt.encode(
        payload=data,
        key=USER_ACCESS_TOKEN_SECRET,
        algorithm='HS256'
    )

    return token



def decode_user_access_token(token: str) -> UserAccessToken:
    payload = jwt.decode(
        jwt=token,
        key=USER_ACCESS_TOKEN_SECRET,
        algorithms=['HS256']
    )

    type = payload['type']
    if type != 'user':
        raise jwt.InvalidTokenError

    expires_at_ts = int(payload['exp'])
    expired = int(now().timestamp()) > expires_at_ts
    if expired:
        raise jwt.InvalidTokenError
    expires_at = datetime.datetime.fromtimestamp(expires_at_ts)

    user_id_str = payload['sub']
    if not user_id_str:
        raise jwt.InvalidTokenError
    user_id = uuid.UUID(user_id_str)

    user_login = payload['login']
    if not isinstance(user_login, str):
        raise jwt.InvalidTokenError

    return UserAccessToken(
        user=UserForAccessToken(id=user_id, login=user_login),
        expires_at=expires_at,
    )