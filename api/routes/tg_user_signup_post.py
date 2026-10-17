from fastapi import Depends, status, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlmodel import Session

from backend_api_model.back_api_tg_user_to_signup import BackApiTgUserToSignup
from backend_api_model.back_api_user_logged_in import BackApiUserLoggedIn
from services.jwt.lib.jwt_tg_user_service import create_tg_user_access_token
from services.jwt.model.tg_user_for_access_token import TgUserForAccessToken
from db.connection.db_connection import get_session
from backend_api_model.back_api_error import BackApiError
from api.convert.back_api_user_from_db_user import back_api_user_from_db_user
from db.model.db_tg_user import DbTgUser
from db.model.db_user import DbUser
from db.repo.tg_user_repo import db_upsert_tg_user
from db.repo.user_repo import db_get_user_by_login
from services.jwt.model.user_for_access_token import UserForAccessToken
from services.pwd_hash.pwd_hash_service import hash_pwd
from utils import datetimes
from pydantic import model_validator
from validators.validate_user_to_signup_pwd import validate_user_to_signup_pwd
from validators.validate_user_to_signup_login import validate_user_to_signup_login

user_signup_router = APIRouter(prefix="/user/signup")


class BackApiTgUserToSignupWithValidation(BackApiTgUserToSignup):
    @model_validator(mode="after")
    def validate_after(self) -> "BackApiTgUserToSignupWithValidation":
        validate_user_to_signup_login(self.login)
        validate_user_to_signup_pwd(self.pwd)
        return self



@user_signup_router.post("", status_code=status.HTTP_201_CREATED, response_model=BackApiUserLoggedIn)
def tg_user_signup_post_route_handler(
        user_to_signup: BackApiTgUserToSignupWithValidation,
        session: Session = Depends(get_session)
):

    # Проверяем, нет ли уже пользователя с таким логином
    db_user = db_get_user_by_login(session, user_to_signup.login)
    if db_user:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(
                BackApiError(
                    error_code="LOGIN_EXISTS",
                    msg="Пользователь с таким логином уже существует",
                )
            )
        )

    # Хэшируем пароль
    hashed_pwd = hash_pwd(user_to_signup.pwd)

    # Создаем модель для БД (UUID сгенерируется автоматически через default_factory)
    db_user = DbUser(
        login=user_to_signup.login,
        pwd_hash=hashed_pwd
    )

    # Сохраняем в PostgreSQL
    session.add(db_user)
    session.commit()

    # Обновляем текущий объект реальными данными из PostgreSQL
    session.refresh(db_user)

    # Create or update tg user & bind tg user to user
    db_tg_user = DbTgUser(
        id=user_to_signup.tg_user.id,
        user_id=db_user.id,
        username=user_to_signup.tg_user.username,
        first_name=user_to_signup.tg_user.first_name,
        last_name=user_to_signup.tg_user.last_name,
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
