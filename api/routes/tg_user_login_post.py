from fastapi import Depends, status, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlmodel import Session

from backend_api_model.back_api_tg_user_to_login import BackApiTgUserLogin
from backend_api_model.back_api_user_logged_in import BackApiUserLoggedIn
from db.connection.db_connection import get_session
from backend_api_model.back_api_error import BackApiError
from api.convert.back_api_user_from_db_user import back_api_user_from_db_user
from db.tables.db_tg_user import DbTgUser
from db.repo.tg_user_repo import db_upsert_tg_user
from db.repo.user_repo import db_get_user_by_login
from services.jwt.lib.jwt_tg_user_service import create_tg_user_access_token
from services.jwt.model.tg_user_for_access_token import TgUserForAccessToken
from services.jwt.model.user_for_access_token import UserForAccessToken
from services.pwd_hash.pwd_hash_service import verify_pwd
from utils import datetimes



tg_user_login_router = APIRouter(prefix="/tg_user/login")


@tg_user_login_router.post("", status_code=status.HTTP_200_OK, response_model=BackApiUserLoggedIn)
def user_login_post_route_handler(
        user_to_login: BackApiTgUserLogin,
        session: Session = Depends(get_session)
):

    db_user = db_get_user_by_login(session, user_to_login.login)

    if not db_user:
        return no_user()

    pwd_is_valid = verify_pwd(user_to_login.pwd, db_user.pwd_hash)

    if not pwd_is_valid:
        return no_user()

    # Create or update tg user & bind tg user to user
    db_tg_user = DbTgUser(
        id=user_to_login.tg_user.id,
        user_id=db_user.id,
        username=user_to_login.tg_user.username,
        first_name=user_to_login.tg_user.first_name,
        last_name=user_to_login.tg_user.last_name,
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

    return BackApiUserLoggedIn(
        access_token=tg_user_access_token,
        user=back_api_user_from_db_user(db_user)
    )



def no_user():
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=jsonable_encoder(
            BackApiError(
                error_code="NO_USER",
                msg="Пользователь с такой парой логин-пароль не найден",
            )
        )
    )
