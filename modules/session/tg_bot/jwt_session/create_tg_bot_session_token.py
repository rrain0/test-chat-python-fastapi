from datetime import datetime
from uuid import UUID

import jwt

from core.config.env import TG_BOT_SESSION_TOKEN_LIFETIME, TG_BOT_SESSION_TOKEN_SECRET
from modules.session.tg_bot.jwt_session.tg_bot_session_token import TgBotSessionToken


def create_tg_bot_session_token(
        id: UUID,
        session_id: UUID,
        created_at: datetime,
        user_id: UUID,
        user_username: str,
        tg_user_id: UUID,
        tg_user_username: str,
):
    lifetime = TG_BOT_SESSION_TOKEN_LIFETIME
    expires_at = created_at + lifetime

    token = TgBotSessionToken(
        type='TgBotSessionToken',
        id=id,
        created_at=created_at,
        expires_at=expires_at,
        session_id=session_id,
        user_id=user_id,
        user_username=user_username,
        tg_user_id=tg_user_id,
        tg_user_username=tg_user_username,
    )

    token_str = jwt.encode(
        payload=token.model_dump(),
        key=TG_BOT_SESSION_TOKEN_SECRET,
        algorithm='HS256'
    )

    token_str = f'tg_bot_{token_str}'

    return token_str, token
