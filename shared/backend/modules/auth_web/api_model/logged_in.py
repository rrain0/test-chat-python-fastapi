from pydantic import BaseModel

from shared.backend.modules.user.api_model.user import BackApiUser


class BackApiWebUserLoggedIn(BaseModel):
    access_token: str
    user: BackApiUser
