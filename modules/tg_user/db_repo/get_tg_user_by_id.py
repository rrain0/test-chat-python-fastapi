from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from modules.tg_user.db_tables.tg_user import PgTgUser


async def get_tg_user_by_id(postgres: AsyncSession, id: int) -> PgTgUser | None:
    return (await postgres.exec(select(PgTgUser).where(PgTgUser.id == id))).first()
