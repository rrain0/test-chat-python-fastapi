from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session

from db_model.db_tg_user import DbTgUser



def upsert_tg_user(session: Session, db_tg_user: DbTgUser) -> None:
    stmt = insert(DbTgUser).values(
        id=db_tg_user.id,
        username=db_tg_user.username,
        first_name=db_tg_user.first_name,
        last_name=db_tg_user.last_name,
    )

    # If the ID already exists, update these fields
    stmt = stmt.on_conflict_do_update(
        index_elements=["id"],
        set_={
            "username": stmt.excluded.username,
            "first_name": stmt.excluded.first_name,
            "last_name": stmt.excluded.last_name,
        }
    )

    session.exec(stmt)
    session.commit()
