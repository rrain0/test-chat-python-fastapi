from uuid import UUID

from sqlmodel import select
from modules.session_web.postgres.tables.web_session import PgWebSession
from shared.utils.postgres.async_postgres import AsyncPostgres


async def pg_get_web_session_by_id_by_user_id(
        id: UUID,
        user_id: UUID,
        postgres: AsyncPostgres,
) -> PgWebSession | None:
    return (await postgres.exec(
        select(PgWebSession)
        .where(PgWebSession.id == id)
        .where(PgWebSession.user_id == user_id)
    )).first()
