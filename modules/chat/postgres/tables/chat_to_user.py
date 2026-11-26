from uuid import UUID

from sqlmodel import Field, SQLModel

from sqlalchemy import Index


class PgChatToUser(SQLModel, table=True):
    __tablename__ = "chat_to_users"

    chat_id: UUID = Field(
        nullable=False,
        primary_key=True,
        index=True,
        foreign_key="chats.id",
    )
    user_id: UUID = Field(
        nullable=False,
        primary_key=True,
        index=True,
        foreign_key="users.id",
    )

    # Index setup via sa_table_args
    __table_args__ = (
        # Index for quickly finding chats of specific user (for EXISTS clause)
        Index("idx_user_id_to_chat_id", "user_id", "chat_id"),

        # An index for quickly checking whether anyone else is in the chat
        Index("idx_chat_id_to_user_id", "chat_id", "user_id"),
    )
