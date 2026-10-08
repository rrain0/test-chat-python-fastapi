import uuid
from pydantic import BaseModel
from db_model.db_user import DbUser



class ApiUser(BaseModel):
    id: uuid.UUID
    login: str



def db_user_to_api_user(db_user: DbUser) -> ApiUser:
    return ApiUser(
        id=db_user.id,
        login=db_user.login,
    )