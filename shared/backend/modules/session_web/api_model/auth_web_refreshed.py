from pydantic import BaseModel


class BackApiAuthWebRefreshed(BaseModel):
    access_token: str
