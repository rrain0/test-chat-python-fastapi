from fastapi import Depends, status, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlmodel import Session

from db_connection.db_connection import get_session
from api_model.api_error import ApiError
from api_model.api_user import ApiUser
from api_model.api_user_from_db_user import api_user_from_db_user
from db_repo.user_repo import db_get_user_by_login
from services.jwt.jwt_user_service import create_user_access_token
from services.jwt.user_for_access_token import UserForAccessToken
from services.pwd_hash_service import verify_pwd
from utils import datetimes



user_login_router = APIRouter(prefix="/user/login")



class ApiUserLogin(BaseModel):
    login: str
    pwd: str

class ApiUserLoggedIn(BaseModel):
    access_token: str
    user: ApiUser



@user_login_router.post("", status_code=status.HTTP_200_OK, response_model=ApiUserLoggedIn)
def user_login_post_route_handler(api_user_login: ApiUserLogin, session: Session = Depends(get_session)):

    db_user = db_get_user_by_login(session, api_user_login.login)

    if not db_user:
        return no_user()

    pwd_is_valid = verify_pwd(api_user_login.pwd, db_user.pwd_hash)

    if not pwd_is_valid:
        return no_user()

    access_token = create_user_access_token(
        user=UserForAccessToken(id=db_user.id, login=db_user.login),
        created_at=datetimes.now()
    )

    return ApiUserLoggedIn(
        access_token=access_token,
        user=api_user_from_db_user(db_user)
    )



def no_user():
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=jsonable_encoder(
            ApiError(
                error_code="NO_USER",
                msg="Пользователь с такой парой логин-пароль не найден",
            )
        )
    )
