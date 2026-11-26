from sqlmodel import select

from modules.user.postgres.tables.user import PgUser
from shared.utils.postgres.async_postgres import AsyncPostgres


async def pg_user_exists_by_username(
        username: str,
        postgres: AsyncPostgres,
) -> bool:
    statement = select(select(PgUser).where(PgUser.username == username).exists())
    return (await postgres.exec(statement)).one()
