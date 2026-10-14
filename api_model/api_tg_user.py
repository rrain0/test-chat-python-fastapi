from pydantic import BaseModel


class ApiTgUser(BaseModel):
    id: int
    username: str | None
    first_name: str
    last_name: str | None
