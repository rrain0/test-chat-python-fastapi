from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from modules.user.postgres.user import PgUser


async def pg_user_exists_by_username(
        username: str,
        postgres: AsyncSession,
) -> bool:
    statement = select(select(PgUser).where(PgUser.username == username).exists())
    return (await postgres.exec(statement)).one()
