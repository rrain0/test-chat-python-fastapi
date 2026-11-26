from uuid import UUID

from redis_fastapi.deps import AsyncClient

from modules.session_web.redis.key.user_session import rd_get_user_web_session_key
from modules.session_web.redis.entity.web_session import RdWebSession


def rd_get_prev_user_web_session_key(user_id: UUID, session_id: UUID):
    return f"{rd_get_user_web_session_key(user_id, session_id)}:prev"


async def rd_get_prev_web_session(
        user_id: UUID,
        session_id: UUID,
        redis: AsyncClient,
) -> RdWebSession | None:
    rd_web_session_json_str = await redis.get(rd_get_prev_user_web_session_key(user_id, session_id))
    if not rd_web_session_json_str:
        return None
    return RdWebSession.model_validate_json(rd_web_session_json_str)


async def rd_set_prev_web_session(
        web_session: RdWebSession,
        redis: AsyncClient,
):
    return await redis.set(
        name=rd_get_prev_user_web_session_key(web_session.user_id, web_session.id),
        value=web_session.model_dump_json(),
        exat=web_session.refresh_token_expires_at,
    )


async def rd_delete_prev_web_session(
        user_id: UUID,
        session_id: UUID,
        redis: AsyncClient,
):
    return await redis.delete(rd_get_prev_user_web_session_key(user_id, session_id))
