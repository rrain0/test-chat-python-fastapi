from fastapi import Depends, status, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlmodel import Session

from api_model.api_tg_user import ApiTgUser
from db_connection.db_connection import get_session
from api_model.api_error import ApiError
from api_model.api_user import ApiUser
from api_model.api_user_from_db_user import api_user_from_db_user
from db_model.db_tg_user import DbTgUser
from db_repo.tg_user_repo import db_upsert_tg_user
from db_repo.user_repo import db_get_user_by_login
from services.jwt import tg_user_access_token
from services.jwt.jwt_tg_user_service import create_tg_user_access_token
from services.jwt.jwt_user_service import create_user_access_token
from services.jwt.tg_user_for_access_token import TgUserForAccessToken
from services.jwt.user_for_access_token import UserForAccessToken
from services.pwd_hash_service import verify_pwd
from utils import datetimes



tg_user_login_router = APIRouter(prefix="/tg_user/login")




class ApiTgUserLogin(BaseModel):
    login: str
    pwd: str
    tg_user: ApiTgUser

class ApiTgUserLoggedIn(BaseModel):
    access_token: str
    user: ApiUser



@tg_user_login_router.post("", status_code=status.HTTP_200_OK, response_model=ApiTgUserLoggedIn)
def user_login_post_route_handler(api_tg_user_login: ApiTgUserLogin, session: Session = Depends(get_session)):

    db_user = db_get_user_by_login(session, api_tg_user_login.login)

    if not db_user:
        return no_user()

    pwd_is_valid = verify_pwd(api_tg_user_login.pwd, db_user.pwd_hash)

    if not pwd_is_valid:
        return no_user()

    db_tg_user = DbTgUser(
        id=api_tg_user_login.tg_user.id,
        user_id=db_user.id,
        username=api_tg_user_login.tg_user.username,
        first_name=api_tg_user_login.tg_user.first_name,
        last_name=api_tg_user_login.tg_user.last_name,
    )
    db_upsert_tg_user(session, db_tg_user)



    tg_user_access_token = create_tg_user_access_token(
        user=UserForAccessToken(
            id=db_user.id,
            login=db_user.login
        ),
        tg_user=TgUserForAccessToken(
            id=db_tg_user.id,
            username=db_tg_user.username,
            first_name=db_tg_user.first_name,
            last_name=db_tg_user.last_name
        ),
        created_at=datetimes.now()
    )

    return ApiTgUserLoggedIn(
        access_token=tg_user_access_token,
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
