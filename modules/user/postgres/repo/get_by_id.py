from uuid import UUID

from sqlmodel import select
from modules.user.postgres.tables.user import PgUser
from shared.utils.postgres.async_postgres import AsyncPostgres


async def pg_get_user_by_id(
        id: UUID,
        postgres: AsyncPostgres,
) -> PgUser | None:
    return (await postgres.exec(select(PgUser).where(PgUser.id == id))).first()
