import datetime
import uuid
from sqlmodel import Field, SQLModel, String



class DbMsg(SQLModel, table=True):
    __tablename__ = "msgs"
    id: uuid.UUID = Field(
        nullable=False,
        primary_key=True,
        index=True,
        default_factory=uuid.uuid4
    )
    chat_id: uuid.UUID = Field(
        nullable=False,
        index=True,
        foreign_key="chats.id",
    )
    sent_at: datetime.datetime = Field(
        nullable=False,
    )
    text_content: str = Field(
        nullable=False,
        sa_type=String(5000),
        min_length=0,
        max_length=5000,
    )
