from uuid import UUID, uuid7
from sqlmodel import Field, SQLModel



class DbChat(SQLModel, table=True):
    __tablename__ = 'chats'
    id: UUID = Field(
        nullable=False,
        primary_key=True,
        index=True,
        default_factory=uuid7
    )
