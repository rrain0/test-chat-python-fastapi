from uuid import uuid7, UUID

from redis_fastapi import AsyncRedisDep
from sqlmodel.ext.asyncio.session import AsyncSession

from modules.session.tg_bot.postgres.get_tg_bot_session_by_tg_user_id import pg_get_tg_bot_session_by_tg_user_id


async def create_tg_bot_session(
        user_id: UUID,
        tg_user_id: int,
        postgres: AsyncSession,
        redis: AsyncRedisDep,
):
    tg_bot_session = await pg_get_tg_bot_session_by_tg_user_id(tg_user_id, postgres)
