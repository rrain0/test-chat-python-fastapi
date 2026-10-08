import datetime
import uuid
import jwt

from env import ACCESS_TOKEN_LIFETIME, ACCESS_TOKEN_SECRET
from utils.datetimes import parse_duration


def create_access_token(
        user_id: uuid.UUID,
        created_at: datetime.datetime,
) -> str:
    lifetime = datetime.timedelta(milliseconds=parse_duration(ACCESS_TOKEN_LIFETIME))
    expires_at = created_at + lifetime

    data = {
        "exp": expires_at.isoformat(),
        "sub": str(user_id),
    }

    token = jwt.encode(
        data,
        ACCESS_TOKEN_SECRET,
        algorithm='HS256'
    )

    return token

