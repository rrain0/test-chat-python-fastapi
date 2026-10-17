from sqlmodel import SQLModel

from db.model.db_chat import DbChatIdPkFk
from db.model.db_user import DbUserIdPkFk


class DbChatToUser(
    DbChatIdPkFk,
    DbUserIdPkFk,
    SQLModel,
    table=True,
):
    __tablename__ = "chat_users"
