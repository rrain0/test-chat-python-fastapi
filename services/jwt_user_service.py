import datetime
import uuid
import jwt
from pydantic import BaseModel

from env import USER_ACCESS_TOKEN_LIFETIME, USER_ACCESS_TOKEN_SECRET
from utils.datetimes import parse_duration, now



class UserAccessToken(BaseModel):
    user_id: uuid.UUID
    expires_at: datetime.datetime



def create_user_access_token(
        user_id: uuid.UUID,
        created_at: datetime.datetime,
) -> str:
    lifetime = datetime.timedelta(milliseconds=parse_duration(USER_ACCESS_TOKEN_LIFETIME))
    expires_at = created_at + lifetime

    data = {
        "type": "user",
        "exp": int(expires_at.timestamp()),
        "sub": str(user_id),
    }

    token = jwt.encode(
        data,
        USER_ACCESS_TOKEN_SECRET,
        algorithm='HS256'
    )

    return token



def decode_user_access_token(token: str) -> UserAccessToken:
    payload = jwt.decode(token, USER_ACCESS_TOKEN_SECRET, algorithms=['HS256'])

    type = payload['type']
    if type != 'user':
        raise jwt.InvalidTokenError

    expires_at_ts = int(payload['exp'])
    expired = int(now().timestamp()) > expires_at_ts
    if expired:
        raise jwt.InvalidTokenError
    expires_at = datetime.datetime.fromtimestamp(expires_at_ts)

    id_str = payload['sub']
    if not id_str:
        raise jwt.InvalidTokenError
    id_uuid = uuid.UUID(id_str)

    return UserAccessToken(
        user_id=id_uuid,
        expires_at=expires_at,
    )