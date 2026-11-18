from datetime import datetime
from uuid import UUID

import jwt

from core.config.env import WEB_ACCESS_TOKEN_LIFETIME, WEB_ACCESS_TOKEN_SECRET
from modules.session.web.jwt_access.web_access_token import WebAccessToken


def create_web_access_token(
        id: UUID,
        session_id: UUID,
        refresh_token_id: UUID,
        created_at: datetime,
        user_id: UUID,
        user_username: str,
):
    lifetime = WEB_ACCESS_TOKEN_LIFETIME
    expires_at = created_at + lifetime

    token = WebAccessToken(
        type='WebAccessToken',
        id=id,
        created_at=created_at,
        expires_at=expires_at,
        session_id=session_id,
        refresh_token_id=refresh_token_id,
        user_id=user_id,
        user_username=user_username,
    )

    token_str = jwt.encode(
        payload=token.model_dump(),
        key=WEB_ACCESS_TOKEN_SECRET,
        algorithm='HS256'
    )

    token_str = f'web_{token_str}'

    return token_str, token
