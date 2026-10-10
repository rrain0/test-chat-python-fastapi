from sqlmodel import Field, SQLModel, String, BigInteger



class DbTgUser(SQLModel, table=True):
    __tablename__ = "tg_users"
    id: int = Field(
        nullable=False,
        sa_type=BigInteger,
        primary_key=True,
        index=True,
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
