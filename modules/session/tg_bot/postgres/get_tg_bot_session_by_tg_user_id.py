from modules.session.tg_bot.postgres.tg_bot_session import PgTgBotSession, PgTgBotSessionUpdate
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.dialects.postgresql import insert


async def pg_upsert_tg_bot_session_by_tg_user_id(
        pg_tg_bot_session: PgTgBotSession,
        pg_tg_bot_session_update: PgTgBotSessionUpdate,
        postgres: AsyncSession,
) -> PgTgBotSession:
    statement = insert(PgTgBotSession).values(**pg_tg_bot_session.model_dump())
    statement = statement.on_conflict_do_update(
        index_elements=["tg_user_id"], # Must be a UNIQUE column or PRIMARY KEY
        set_=pg_tg_bot_session_update.model_dump(exclude_unset=True)
    ).returning(PgTgBotSession)
    return (await postgres.exec(statement)).scalar_one()
