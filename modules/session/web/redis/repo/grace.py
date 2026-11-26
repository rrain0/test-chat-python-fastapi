from datetime import datetime
from uuid import UUID

from redis_fastapi.deps import AsyncClient

from core.config.env import WEB_REFRESH_TOKEN_GRACE_PERIOD
from modules.session.web.redis.key.keys import rd_get_user_web_session_key
from modules.session.web.redis.entity.web_session import RdWebSession


def rd_get_grace_user_web_session_key(user_id: UUID, session_id: UUID):
    return f"{rd_get_user_web_session_key(user_id, session_id)}:grace"


async def rd_get_grace_web_session(
        user_id: UUID,
        session_id: UUID,
        redis: AsyncClient,
) -> RdWebSession | None:
    rd_web_session_json_str = await redis.get(rd_get_grace_user_web_session_key(user_id, session_id))
    if not rd_web_session_json_str:
        return None
    return RdWebSession.model_validate_json(rd_web_session_json_str)


async def rd_set_grace_web_session(
        web_session: RdWebSession,
        grace_start_at: datetime,
        redis: AsyncClient,
):
    return await redis.set(
        name=rd_get_grace_user_web_session_key(web_session.user_id, web_session.id),
        value=web_session.model_dump_json(),
        exat=min(grace_start_at + WEB_REFRESH_TOKEN_GRACE_PERIOD, web_session.refresh_token_expires_at)
    )


async def rd_delete_grace_web_session(
        user_id: UUID,
        session_id: UUID,
        redis: AsyncClient,
):
    return await redis.delete(rd_get_grace_user_web_session_key(user_id, session_id))
