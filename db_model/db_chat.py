import uuid
from sqlmodel import Field, SQLModel, String



class DbChat(SQLModel, table=True):
    __tablename__ = "chats"
    id: uuid.UUID = Field(
        nullable=False,
        primary_key=True,
        index=True,
        default_factory=uuid.uuid4
    )



class DbChatIdPkFk(SQLModel):
    chat_id: uuid.UUID = Field(
        nullable=False,
        primary_key=True,
        index=True,
        foreign_key="chats.id",
    )

class DbChatIdFk(SQLModel):
    chat_id: uuid.UUID = Field(
        nullable=False,
        index=True,
        foreign_key="chats.id",
    )
