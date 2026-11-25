from uuid import UUID
from sqlmodel import Field, SQLModel, String

#TODO updated_at everywhere

class PgUser(SQLModel, table=True):
    __tablename__ = "users"
    id: UUID = Field(
        nullable=False,
        primary_key=True,
        index=True,
    )
    username: str = Field(
        sa_type=String(32),
        nullable=False,
        index=True,
        unique=True,
        min_length=4,
        max_length=32,
    )
    pwd_hash: str = Field(
        sa_type=String(60),
        nullable=False,
    )

