from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from modules.session.web.postgres.web_session import PgWebSession


async def pg_upsert_web_session_by_id(
        pg_web_session: PgWebSession,
        postgres: AsyncSession,
) -> None:
    # updated_at must be already define earlier
    statement = insert(PgWebSession).values(**pg_web_session.model_dump())

    statement = statement.on_conflict_do_update(
        index_elements=["id"],
        set_={
            # "id" is not updated
            # "created_at" is not updated
            "updated_at": statement.excluded.updated_at,
            "refresh_token_id": statement.excluded.refresh_token_id,
            "refresh_token_created_at": statement.excluded.refresh_token_created_at,
            "refresh_token_expires_at": statement.excluded.refresh_token_expires_at,
            # "user_id" is not updated
            "last_active_at": statement.excluded.last_active_at,
            "last_active_at_ip": statement.excluded.last_active_at_ip,
            "last_active_at_device": statement.excluded.last_active_at_device,
        }
    )

    await postgres.exec(statement)
