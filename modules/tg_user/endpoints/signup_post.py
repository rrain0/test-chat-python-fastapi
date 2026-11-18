from uuid import uuid7

from fastapi import status, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from shared.backend.modules.tg_user.api_model.tg_user_to_signup import BackApiTgUserToSignup
from shared.backend.modules.user.api_model.user_logged_in import BackApiUserLoggedIn
from services.jwt.lib.jwt_tg_user_service import create_tg_user_access_token
from services.jwt.model.tg_user_for_access_token import TgUserForAccessToken
from core.postgres.init import AsyncPostgresDep
from shared.backend.modules.error.api_model.error import BackApiError
from modules.user.convert.db_user_to_back_api_user import db_user_to_back_api_user
from modules.tg_user.db_tables.tg_user import PgTgUser
from modules.user.postgres.user import PgUser
from modules.tg_user.db_repo.upsert_tg_user import pg_upsert_tg_user_by_id
from modules.user.postgres.get_user_by_username import pg_get_user_by_username
from services.jwt.model.user_for_access_token import UserForAccessToken
from modules.pwd_hash.pwd_hash import hash_pwd
from shared.utils.datetimes.now import now
from pydantic import model_validator
from validators.user_to_signup_pwd import validate_user_to_signup_pwd
from validators.user_to_signup_username import validate_user_to_signup_username

router_tg_user_signup = APIRouter(prefix='/api/tg_user/signup')


class BackApiTgUserToSignupWithValidation(BackApiTgUserToSignup):
    @model_validator(mode='after')
    def validate_after(self) -> 'BackApiTgUserToSignupWithValidation':
        validate_user_to_signup_username(self.username)
        validate_user_to_signup_pwd(self.pwd)
        return self



@router_tg_user_signup.post("", status_code=status.HTTP_201_CREATED, response_model=BackApiUserLoggedIn)
async def tg_user_signup_post(
        user_to_signup: BackApiTgUserToSignupWithValidation,
        postgres: AsyncPostgresDep,
):

    # Проверяем, нет ли уже пользователя с таким логином
    db_user = await pg_get_user_by_username(user_to_signup.username, postgres)
    if db_user:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(
                BackApiError(
                    error_code='USERNAME_EXISTS',
                    error_msg='Пользователь с таким логином уже существует',
                )
            )
        )

    # Хэшируем пароль
    hashed_pwd = hash_pwd(user_to_signup.pwd)

    # Создаем модель для БД (UUID сгенерируется автоматически через default_factory)
    db_user = PgUser(
        id=uuid7(),
        username=user_to_signup.username,
        pwd_hash=hashed_pwd
    )

    # Сохраняем в PostgreSQL
    postgres.add(db_user)
    await postgres.commit()

    # Обновляем текущий объект реальными данными из PostgreSQL
    await postgres.refresh(db_user)

    # Create or update tg user & bind tg user to user
    db_tg_user = PgTgUser(
        id=user_to_signup.tg_user.id,
        user_id=db_user.id,
        username=user_to_signup.tg_user.username,
        first_name=user_to_signup.tg_user.first_name,
        last_name=user_to_signup.tg_user.last_name,
    )
    await pg_upsert_tg_user_by_id(db_tg_user, postgres)
    await postgres.commit()



    tg_user_access_token = create_tg_user_access_token(
        user=UserForAccessToken(
            id=db_user.id,
            username=db_user.username
        ),
        tg_user=TgUserForAccessToken(
            id=db_tg_user.id,
            username=db_tg_user.username,
            first_name=db_tg_user.first_name,
            last_name=db_tg_user.last_name
        ),
        created_at=now()
    )

    return BackApiUserLoggedIn(
        access_token=tg_user_access_token,
        user=db_user_to_back_api_user(db_user)
    )
