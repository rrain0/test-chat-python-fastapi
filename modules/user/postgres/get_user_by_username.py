from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from modules.user.postgres.user import PgUser


async def pg_get_user_by_username(
        username: str,
        postgres: AsyncSession,
) -> PgUser | None:
    return (await postgres.exec(select(PgUser).where(PgUser.username == username))).first()
