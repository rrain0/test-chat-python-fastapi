from uuid import uuid7, UUID

from redis_fastapi import AsyncRedisDep
from sqlmodel.ext.asyncio.session import AsyncSession

from modules.session.tg_bot.postgres.get_tg_bot_session_by_tg_user_id import pg_upsert_tg_bot_session_by_tg_user_id
from modules.session.tg_bot.postgres.tg_bot_session import PgTgBotSession, PgTgBotSessionUpdate
from shared.utils.datetimes.duration import duration
from shared.utils.datetimes.now import now


async def create_tg_bot_session(
        user_id: UUID,
        tg_user_id: int,
        postgres: AsyncSession,
        redis: AsyncRedisDep,
):
    at = now()
    session_expires_at = at + duration("2y")
    tg_bot_session = await pg_upsert_tg_bot_session_by_tg_user_id(
        pg_tg_bot_session=PgTgBotSession(
            id=uuid7(),
            created_at=at,
            updated_at=at,
            session_expires_at=session_expires_at,
            user_id=user_id,
            tg_user_id=tg_user_id,
            last_active_at=at,
        ),
        pg_tg_bot_session_update=PgTgBotSessionUpdate(
            updated_at=at,
            session_expires_at=session_expires_at,
            last_active_at=at,
        ),
        postgres=postgres,
    )
