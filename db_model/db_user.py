import uuid
from sqlmodel import Field, SQLModel, String



class DbUser(
    SQLModel,
    table=True,
):
    __tablename__ = "users"
    id: uuid.UUID = Field(
        nullable=False,
        primary_key=True,
        index=True,
        default_factory=uuid.uuid4
    )
    login: str = Field(
        nullable=False,
        sa_type=String(30),
        index=True,
        unique=True,
        min_length=1,
        max_length=30
    )
    pwd_hash: str = Field(
        nullable=False,
        sa_type=String(60),
    )



class DbUserIdPkFk(SQLModel):
    user_id: uuid.UUID = Field(
        nullable=False,
        primary_key=True,
        index=True,
        foreign_key="users.id",
    )

class DbUserIdFk(SQLModel):
    user_id: uuid.UUID = Field(
        nullable=False,
        index=True,
        foreign_key="users.id",
    )
