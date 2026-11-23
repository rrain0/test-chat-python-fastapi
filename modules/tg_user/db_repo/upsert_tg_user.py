from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from modules.tg_user.db_tables.tg_user import PgTgUser


async def pg_upsert_tg_user_by_id(
        pg_tg_user: PgTgUser,
        postgres: AsyncSession,
) -> None:
    statement = insert(PgTgUser).values(**pg_tg_user.model_dump())

    # If the ID already exists, update these fields
    statement = statement.on_conflict_do_update(
        index_elements=["id"],
        set_={
            "user_id": statement.excluded.user_id,
            "username": statement.excluded.username,
            "first_name": statement.excluded.first_name,
            "last_name": statement.excluded.last_name,
        }
    )

    await postgres.exec(statement)
