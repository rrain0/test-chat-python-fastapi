from uuid import UUID

from redis_fastapi.deps import AsyncClient

from core.config.env import REDIS_PREFIX
from modules.session.web.redis.web_session import RdWebSessionByToken


def rd_get_user_web_session_key(user_id: UUID, session_id: UUID):
    return (
        f'{REDIS_PREFIX}:session:web'
        f':user_id:{str(user_id)}'
        f':session_id:{str(session_id)}'
        f':current'
    )


async def rd_get_web_session(
        user_id: UUID,
        session_id: UUID,
        redis: AsyncClient,
) -> RdWebSessionByToken | None:
    rd_web_session_json_str = await redis.get(rd_get_user_web_session_key(user_id, session_id))
    if not rd_web_session_json_str:
        return None
    return RdWebSessionByToken.model_validate_json(rd_web_session_json_str)


async def rd_set_web_session(
        web_session: RdWebSessionByToken,
        redis: AsyncClient,
):
    return await redis.set(
        name=rd_get_user_web_session_key(web_session.user_id, web_session.id),
        value=web_session.model_dump_json(),
        exat=web_session.refresh_token_expires_at,
    )


async def rd_delete_web_session(
        user_id: UUID,
        session_id: UUID,
        redis: AsyncClient,
):
    return await redis.delete(rd_get_user_web_session_key(user_id, session_id))
