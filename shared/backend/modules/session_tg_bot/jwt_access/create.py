from datetime import datetime
from uuid import UUID

import jwt

from core.config.env import TG_BOT_ACCESS_TOKEN_LIFETIME, TG_BOT_ACCESS_TOKEN_SECRET
from shared.backend.modules.session_tg_bot.jwt_access.token import TgBotAccessToken


def create_tg_bot_access_token(
        id: UUID,
        created_at: datetime,
        tg_user_id: int,
        tg_user_username: str,
):
    lifetime = TG_BOT_ACCESS_TOKEN_LIFETIME
    expires_at = created_at + lifetime

    token = TgBotAccessToken(
        type="TgBotAccessToken",
        id=id,
        created_at=created_at,
        expires_at=expires_at,
        tg_user_id=tg_user_id,
        tg_user_username=tg_user_username,
    )

    token_str = jwt.encode(
        payload=token.model_dump(),
        key=TG_BOT_ACCESS_TOKEN_SECRET,
        algorithm="HS256"
    )

    token_str = f"tg_bot_{token_str}"

    return token_str, token
