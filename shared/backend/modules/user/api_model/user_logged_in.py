from pydantic import BaseModel

from shared.backend.modules.user.api_model.user import BackApiUser


class BackApiUserLoggedIn(BaseModel):
    access_token: str
    user: BackApiUser
