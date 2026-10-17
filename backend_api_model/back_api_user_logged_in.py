from pydantic import BaseModel

from backend_api_model.back_api_user import BackApiUser


class BackApiUserLoggedIn(BaseModel):
    access_token: str
    user: BackApiUser
