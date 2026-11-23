from uuid import UUID

from sqlmodel import Field, SQLModel, String, BigInteger


class PgTgUser(SQLModel, table=True):
    __tablename__ = "tg_users"
    id: int = Field(
        nullable=False,
        sa_type=BigInteger,
        primary_key=True,
        index=True,
    )
    user_id: UUID = Field(
        nullable=False,
        index=True,
        foreign_key="users.id",
    )
    username: str | None = Field(
        nullable=True,
        sa_type=String(32),
        default=None,
    )
    first_name: str = Field(
        nullable=False,
        sa_type=String(64),
    )
    last_name: str | None = Field(
        nullable=True,
        sa_type=String(64),
        default=None,
    )
