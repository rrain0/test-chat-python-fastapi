from sqlmodel import SQLModel

from db_model.db_chat import DbChatIdPkFk
from db_model.db_user import DbUserIdPkFk


class DbChatToUser(
    DbChatIdPkFk,
    DbUserIdPkFk,
    SQLModel,
    table=True,
):
    __tablename__ = "chat_users"
