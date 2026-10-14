from pydantic import BaseModel



class TgUserForAccessToken(BaseModel):
    id: int
    username: str | None
    first_name: str
    last_name: str | None
