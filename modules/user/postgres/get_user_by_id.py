from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from modules.user.postgres.user import PgUser


async def pg_get_user_by_id(
        id: UUID,
        postgres: AsyncSession,
) -> PgUser | None:
    return (await postgres.exec(select(PgUser).where(PgUser.id == id))).first()
