from modules.session.tg_bot.postgres.tg_bot_session import PgTgBotSession
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select


async def pg_get_tg_bot_session_by_tg_user_id(
        tg_user_id: int,
        postgres: AsyncSession,
) -> PgTgBotSession | None:
    return (await postgres.exec(
        select(PgTgBotSession)
        .where(PgTgBotSession.tg_user_id == tg_user_id)
    )).first()
