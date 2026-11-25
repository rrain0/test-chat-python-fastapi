from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel, String


class PgWebSession(SQLModel, table=True):
    __tablename__ = "web_sessions"
    id: UUID = Field(
        nullable=False,
        primary_key=True,
        index=True,
    )

    created_at: datetime = Field(
        nullable=False,
    )
    # Time of real write in postgres, not in redis
    updated_at: datetime = Field(
        nullable=False,
    )

    refresh_token_id: UUID = Field(
        nullable=False,
    )
    refresh_token_created_at: datetime = Field(
        nullable=False,
    )
    refresh_token_expires_at: datetime = Field(
        nullable=False,
    )

    user_id: UUID = Field(
        nullable=False,
        index=True,
        foreign_key="users.id",
    )

    last_active_at: datetime = Field(
        nullable=False,
    )
    last_active_at_ip: str | None = Field(
        nullable=True,
        sa_type=String(100),
    )
    # For web: user agent string
    # For tg bot: "Telegram Bot"
    last_active_at_device: str | None = Field(
        nullable=True,
        sa_type=String(250),
    )



class PgWebSessionUpdate(SQLModel):
    updated_at: Optional[datetime] = None

    refresh_token_id: Optional[UUID] = None
    refresh_token_created_at: Optional[datetime] = None
    refresh_token_expires_at: Optional[datetime] = None

    last_active_at: Optional[datetime] = None
    last_active_at_ip: Optional[str | None] = None
    last_active_at_device: Optional[str | None] = None
