from uuid import UUID

from sqlmodel import delete
from modules.session.web.postgres.table.web_session import PgWebSession
from shared.utils.postgres.async_postgres import AsyncPostgres


async def pg_delete_web_session_by_id(
        id: UUID,
        postgres: AsyncPostgres,
):
    await postgres.exec(delete(PgWebSession).where(PgWebSession.id == id))
