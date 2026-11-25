from fastapi import status, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from shared.backend.modules.tg_user.api_model.tg_user_to_login import BackApiTgUserToLogin
from shared.backend.modules.user.api_model.user_logged_in import BackApiUserLoggedIn
from core.postgres.init import AsyncPostgresDep
from shared.backend.modules.error.api_model.error import BackApiError
from modules.user.convert.pg_user_to_back_api_user import pg_user_to_back_api_user
from modules.tg_user.db_tables.tg_user import PgTgUser
from modules.tg_user.db_repo.upsert_tg_user import pg_upsert_tg_user_by_id
from modules.user.postgres.get_user_by_username import pg_get_user_by_username
from services.jwt.lib.jwt_tg_user_service import create_tg_user_access_token
from services.jwt.model.tg_user_for_access_token import TgUserForAccessToken
from services.jwt.model.user_for_access_token import UserForAccessToken
from modules.pwd_hash.pwd_hash import verify_pwd_athread
from shared.utils.datetimes.now import now

router_tg_user_login = APIRouter(prefix="/api/tg_user/login")


@router_tg_user_login.post("", status_code=status.HTTP_200_OK, response_model=BackApiUserLoggedIn)
async def tg_user_login_post(
        user_to_login: BackApiTgUserToLogin,
        postgres: AsyncPostgresDep,
):
    db_user = await pg_get_user_by_username(user_to_login.login, postgres)

    if not db_user:
        return no_user()

    pwd_is_valid = await verify_pwd_athread(user_to_login.pwd, db_user.pwd_hash)

    if not pwd_is_valid:
        return no_user()

    # Create or update tg user & bind tg user to user
    db_tg_user = PgTgUser(
        id=user_to_login.tg_user.id,
        user_id=db_user.id,
        username=user_to_login.tg_user.username,
        first_name=user_to_login.tg_user.first_name,
        last_name=user_to_login.tg_user.last_name,
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
        user=pg_user_to_back_api_user(db_user)
    )



def no_user():
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=jsonable_encoder(
            BackApiError(
                error_code="NO_USER",
                error_msg="Пользователь с такой парой логин-пароль не найден",
            )
        )
    )
