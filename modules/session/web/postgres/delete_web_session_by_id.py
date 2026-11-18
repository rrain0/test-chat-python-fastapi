from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import delete
from modules.session.web.postgres.web_session import PgWebSession


async def pg_delete_web_session_by_id(
        id: UUID,
        postgres: AsyncSession,
):
    await postgres.exec(delete(PgWebSession).where(PgWebSession.id == id))
