import uuid
from sqlmodel import Field, SQLModel



class DbChat(SQLModel, table=True):
    __tablename__ = "chats"
    id: uuid.UUID = Field(
        nullable=False,
        primary_key=True,
        index=True,
        default_factory=uuid.uuid4
    )
