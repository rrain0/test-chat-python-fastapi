import datetime
import uuid
import jwt
from pydantic import BaseModel

from env import ACCESS_TOKEN_LIFETIME, ACCESS_TOKEN_SECRET
from utils.datetimes import parse_duration


def create_access_token(
        user_id: uuid.UUID,
        created_at: datetime.datetime,
) -> str:
    lifetime = datetime.timedelta(milliseconds=parse_duration(ACCESS_TOKEN_LIFETIME))
    expires_at = created_at + lifetime

    data = {
        "sub": str(user_id),
        "exp": int(expires_at.timestamp()),
    }

    token = jwt.encode(
        data,
        ACCESS_TOKEN_SECRET,
        algorithm='HS256'
    )

    return token



class AccessToken(BaseModel):
    user_id: uuid.UUID
    expires_at: datetime.datetime

def decode_access_token(token: str) -> AccessToken:
    payload = jwt.decode(token, ACCESS_TOKEN_SECRET, algorithms=['HS256'])

    id_str = payload['sub']
    if not id_str:
        raise jwt.InvalidTokenError
    id_uuid = uuid.UUID(id_str)

    expires_at = datetime.datetime.now() + datetime.timedelta(seconds=int(payload['exp']))

    return AccessToken(
        user_id=id_uuid,
        expires_at=expires_at,
    )