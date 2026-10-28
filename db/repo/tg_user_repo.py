from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session, select

from db.tables.db_tg_user import DbTgUser



def db_get_tg_user_by_id(session: Session, id: int) -> DbTgUser | None:
    return session.exec(select(DbTgUser).where(DbTgUser.id == id)).first()

def db_upsert_tg_user(session: Session, db_tg_user: DbTgUser) -> None:
    statement = insert(DbTgUser).values(
        id=db_tg_user.id,
        user_id=db_tg_user.user_id,
        username=db_tg_user.username,
        first_name=db_tg_user.first_name,
        last_name=db_tg_user.last_name,
    )

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

    session.exec(statement)
    session.commit()
