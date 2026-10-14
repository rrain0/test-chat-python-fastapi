import datetime
import uuid
from sqlmodel import Field, SQLModel, String

from db_model.db_chat import DbChatIdFk



class DbMessage(
    DbChatIdFk,
    SQLModel,
    table=True,
):
    __tablename__ = "messages"
    id: uuid.UUID = Field(
        nullable=False,
        primary_key=True,
        index=True,
        default_factory=uuid.uuid4
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
