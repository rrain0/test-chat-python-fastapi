from datetime import datetime
from uuid import UUID

from sqlmodel import Field, SQLModel, String, BigInteger


class PgTgBotSession(SQLModel, table=True):
    __tablename__ = 'tg_bot_sessions'
    id: UUID = Field(
        nullable=False,
        primary_key=True,
        index=True,
    )

    created_at: datetime = Field(
        nullable=False,
    )
    updated_at: datetime = Field(
        nullable=False,
    )

    session_token_id: UUID = Field(
        nullable=False,
    )
    session_token_expires_at: datetime = Field(
        nullable=False,
    )

    user_id: UUID = Field(
        nullable=False,
        index=True,
        foreign_key='users.id',
    )
    tg_user_id: int = Field(
        nullable=False,
        sa_type=BigInteger,
        index=True,
    )

    last_active_at: datetime = Field(
        nullable=False,
    )
    last_active_at_ip: str = Field(
        nullable=False,
        sa_type=String(100),
    )
    last_active_at_device: str = Field(
        nullable=False,
        sa_type=String(250),
    )
