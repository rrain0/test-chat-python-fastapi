from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from modules.session.web.postgres.web_session import PgWebSession, PgWebSessionUpdate


async def pg_upsert_web_session_by_id(
        pg_web_session: PgWebSession,
        pg_web_session_update: PgWebSessionUpdate,
        postgres: AsyncSession,
) -> None:
    # updated_at must be already define earlier
    statement = insert(PgWebSession).values(**pg_web_session.model_dump())

    statement = statement.on_conflict_do_update(
        index_elements=["id"],
        set_=pg_web_session_update.model_dump(exclude_unset=True),
    )

    await postgres.exec(statement)
