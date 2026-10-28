from fastapi import Depends, status, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlmodel import Session

from backend_api_model.back_api_user_logged_in import BackApiUserLoggedIn
from backend_api_model.back_api_user_to_login import BackApiUserToLogin
from db.setup.db_setup import get_session
from backend_api_model.back_api_error import BackApiError
from api.convert.back_api_user_from_db_user import back_api_user_from_db_user
from db.repo.user_repo import db_get_user_by_login
from services.jwt.lib.jwt_user_service import create_user_access_token
from services.jwt.model.user_for_access_token import UserForAccessToken
from services.pwd_hash.pwd_hash_service import verify_pwd
from utils import datetimes



user_login_router = APIRouter(prefix="/user/login")



@user_login_router.post("", status_code=status.HTTP_200_OK, response_model=BackApiUserLoggedIn)
def user_login_post_route_handler(
        user_to_login: BackApiUserToLogin,
        session: Session = Depends(get_session)
):

    db_user = db_get_user_by_login(session, user_to_login.login)

    if not db_user:
        return no_user()

    pwd_is_valid = verify_pwd(user_to_login.pwd, db_user.pwd_hash)

    if not pwd_is_valid:
        return no_user()

    access_token = create_user_access_token(
        user=UserForAccessToken(id=db_user.id, login=db_user.login),
        created_at=datetimes.now()
    )

    return BackApiUserLoggedIn(
        access_token=access_token,
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
