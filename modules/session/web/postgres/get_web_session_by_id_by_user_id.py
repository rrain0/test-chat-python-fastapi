from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from modules.session.web.postgres.web_session import PgWebSession


async def pg_get_web_session_by_id_by_user_id(
        id: UUID,
        user_id: UUID,
        postgres: AsyncSession,
) -> PgWebSession | None:
    return (await postgres.exec(
        select(PgWebSession)
        .where(PgWebSession.id == id)
        .where(PgWebSession.user_id == user_id)
    )).first()
