from sqlmodel import select

from modules.tg_user.db_tables.tg_user import PgTgUser
from shared.utils.postgres.async_postgres import AsyncPostgres


async def get_tg_user_by_id(postgres: AsyncPostgres, id: int) -> PgTgUser | None:
    return (await postgres.exec(select(PgTgUser).where(PgTgUser.id == id))).first()
