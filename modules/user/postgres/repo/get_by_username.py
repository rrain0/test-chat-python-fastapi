from sqlmodel import select

from modules.user.postgres.tables.user import PgUser
from shared.utils.postgres.async_postgres import AsyncPostgres


async def pg_get_user_by_username(
        username: str,
        postgres: AsyncPostgres,
) -> PgUser | None:
    return (await postgres.exec(select(PgUser).where(PgUser.username == username))).first()
