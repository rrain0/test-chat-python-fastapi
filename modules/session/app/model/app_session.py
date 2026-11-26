from uuid import UUID

from pydantic import BaseModel

from shared.backend.modules.session.tg_bot.jwt_access.token import TgBotAccessToken
from modules.session.web.jwt_access.token import WebAccessToken


class AppSession(BaseModel):
    session_id: UUID
    user_id: UUID
    user_username: str

    web_access_token: WebAccessToken | None = None

    tg_bot_access_token: TgBotAccessToken | None = None

