from uuid import uuid7, UUID

from modules.session_web.mappers.pg_to_rd_web_session import pg_to_rd_web_session
from modules.session_web.jwt_access.create import create_web_access_token
from modules.session_web.jwt_refresh.create import create_web_refresh_token
from modules.session_web.postgres.tables.web_session import PgWebSession
from modules.session_web.redis.repo.current import rd_set_current_web_session
from shared.utils.datetimes.now import now
from shared.utils.postgres.async_postgres import AsyncPostgres
from shared.utils.rediss.async_redis import AsyncRedis


async def commit_create_web_session(
        user_id: UUID,
        user_username: str,
        user_ip: str | None,
        user_agent_str: str | None,
        postgres: AsyncPostgres,
        redis: AsyncRedis,
):
    session_id = uuid7()
    session_created_at = now()

    refresh_token_id = uuid7()
    refresh_token_str, refresh_token = create_web_refresh_token(
        id=refresh_token_id,
        session_id=session_id,
        created_at=session_created_at,
        user_id=user_id,
        user_username=user_username,
    )

    pg_session = PgWebSession(
        id=session_id,
        created_at=session_created_at,
        updated_at=session_created_at,
        refresh_token_id=refresh_token.id,
        refresh_token_created_at=refresh_token.created_at,
        refresh_token_expires_at=refresh_token.expires_at,
        user_id=user_id,
        last_active_at=session_created_at,
        last_active_at_ip=user_ip,
        last_active_at_device=user_agent_str,
    )

    access_token_id = uuid7()
    access_token_str, access_token = create_web_access_token(
        id=access_token_id,
        session_id=refresh_token.session_id,
        refresh_token_id=refresh_token.id,
        created_at=session_created_at,
        user_id=user_id,
        user_username=user_username,
    )

    postgres.add(pg_session)
    await postgres.commit()

    rd_session = pg_to_rd_web_session(pg_session)
    await rd_set_current_web_session(
        web_session=rd_session,
        redis=redis,
    )

    return (
        access_token_str,
        access_token,
        refresh_token_str,
        refresh_token,
    )

