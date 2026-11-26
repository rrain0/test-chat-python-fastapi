from uuid import UUID
from sqlmodel import Field, SQLModel



class PgChat(SQLModel, table=True):
    __tablename__ = "chats"
    id: UUID = Field(
        nullable=False,
        primary_key=True,
        index=True,
    )
