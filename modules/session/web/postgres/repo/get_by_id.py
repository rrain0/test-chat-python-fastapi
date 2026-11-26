from uuid import UUID

from sqlmodel import select
from modules.session.web.postgres.table.web_session import PgWebSession
from shared.utils.postgres.async_postgres import AsyncPostgres


async def pg_get_web_session_by_id(
        id: UUID,
        postgres: AsyncPostgres,
) -> PgWebSession | None:
    return (await postgres.exec(select(PgWebSession).where(PgWebSession.id == id))).first()
