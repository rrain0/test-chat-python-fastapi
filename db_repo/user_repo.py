import uuid

from sqlmodel import Session, select
from db_model.db_user import DbUser



def user_by_login(session: Session, login: str) -> DbUser | None:
    return session.exec(select(DbUser).where(DbUser.login == login)).first()

def user_by_id(session: Session, id: uuid.UUID) -> DbUser | None:
    return session.exec(select(DbUser).where(DbUser.id == id)).first()
