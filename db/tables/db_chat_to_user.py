import uuid

from sqlmodel import Field, SQLModel

from sqlalchemy import Index


class DbChatToUser(SQLModel, table=True):
    __tablename__ = "chat_to_users"

    chat_id: uuid.UUID = Field(
        nullable=False,
        primary_key=True,
        index=True,
        foreign_key="chats.id",
    )
    user_id: uuid.UUID = Field(
        nullable=False,
        primary_key=True,
        index=True,
        foreign_key="users.id",
    )

    # Настройка индексов через sa_table_args
    __table_args__ = (
        # 1. Индекс для быстрого поиска чатов конкретного пользователя (для нашего EXISTS)
        Index("idx_user_id_to_chat_id", "user_id", "chat_id"),

        # 2. Индекс для быстрой проверки, есть ли в чате кто-то еще
        Index("idx_chat_id_to_user_id", "chat_id", "user_id"),
    )
