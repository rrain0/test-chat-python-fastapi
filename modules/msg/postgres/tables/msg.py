import datetime
from uuid import UUID
from sqlmodel import Field, SQLModel, String



class DbMsg(SQLModel, table=True):
    __tablename__ = "msgs"
    id: UUID = Field(
        nullable=False,
        primary_key=True,
        index=True,
    )
    chat_id: UUID = Field(
        nullable=False,
        index=True,
        foreign_key="chats.id",
    )
    sent_at: datetime.datetime = Field()
    text_content: str = Field(
        sa_type=String(5000),
        nullable=False,
        min_length=0,
        max_length=5000,
    )
