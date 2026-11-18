from uuid import UUID

from redis_fastapi import AsyncRedisDep
from sqlmodel.ext.asyncio.session import AsyncSession

from modules.session.web.postgres.delete_web_session_by_id import pg_delete_web_session_by_id
from modules.session.web.redis.repo_grace_web_session import rd_delete_grace_web_session
from modules.session.web.redis.repo_prev_web_session import rd_delete_prev_web_session
from modules.session.web.redis.repo_web_session import rd_delete_web_session


async def commit_remove_web_session(
        user_id: UUID,
        session_id: UUID,
        postgres: AsyncSession,
        redis: AsyncRedisDep,
):
    await pg_delete_web_session_by_id(session_id, postgres)
    await postgres.commit()
    # TODO Redis transaction
    await rd_delete_web_session(user_id, session_id, redis)
    await rd_delete_prev_web_session(user_id, session_id, redis)
    await rd_delete_grace_web_session(user_id, session_id, redis)



