from fastapi import status, APIRouter
from fastapi import Request, Response

from modules.session.tg_bot.token_store.access_token import get_tg_bot_access_token
from modules.session.web.repo.create_web_session import commit_create_web_session
from modules.user.postgres.user import PgUser
from shared.backend.modules.user.api_model.user_logged_in import BackApiUserLoggedIn
from shared.backend.modules.user.api_model.user_to_login import BackApiUserToLogin
from core.postgres.init import AsyncPostgresDep
from modules.user.convert.pg_user_to_back_api_user import pg_user_to_back_api_user
from modules.session.web.token_store.refresh_token import add_web_refresh_token
from modules.user.postgres.get_user_by_username import pg_get_user_by_username
from modules.pwd_hash.pwd_hash import verify_pwd_athread
from shared.utils.fastapis.api_error_case import ApiErrorCase
from shared.utils.fastapis.get_client_ip import get_client_ip
from shared.utils.fastapis.get_client_user_agent_str import get_client_user_agent_str
from redis_fastapi import AsyncRedisDep
from sqlmodel.ext.asyncio.session import AsyncSession

from shared.utils.fastapis.auth_header_not_exists import auth_header_not_exists


router_user_login = APIRouter(prefix="/api/user/login")


# Respond 400 instead of 401 because you don't need credentials to access this endpoint
responses = { }
invalid_authorization_type_error = ApiErrorCase(
    status_code=status.HTTP_400_BAD_REQUEST,
    error_code="INVALID_AUTHORIZATION_TYPE",
    error_msg="Authorization header does not match any valid authorization type",
).add_example_to_openapi_responses(responses)
invalid_credentials_error = ApiErrorCase(
    status_code=status.HTTP_400_BAD_REQUEST,
    error_code="INVALID_CREDENTIALS",
    error_msg="User with these login & password was not found",
).add_example_to_openapi_responses(responses)


@router_user_login.post(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=BackApiUserLoggedIn,
    responses=responses,
)
async def user_login_post(
        user_to_login: BackApiUserToLogin,
        request: Request,
        response: Response,
        postgres: AsyncPostgresDep,
        redis: AsyncRedisDep,
):
    # Tg Bot Auth
    tg_bot_access_token_str = get_tg_bot_access_token(request)
    if tg_bot_access_token_str:
        raise "not implemented"


    # Web Auth
    if auth_header_not_exists(request):
        pg_user = await verify_credentials(user_to_login.login, user_to_login.pwd, postgres)

        access_token_str, access_token, refresh_token_str, refresh_token = \
            await commit_create_web_session(
                user_id=pg_user.id,
                user_username=pg_user.username,
                user_ip=get_client_ip(request),
                user_agent_str=get_client_user_agent_str(request),
                postgres=postgres,
                redis=redis,
            )

        add_web_refresh_token(response, refresh_token_str, refresh_token.expires_at)
        return BackApiUserLoggedIn(
            access_token=access_token_str,
            user=pg_user_to_back_api_user(pg_user)
        )


    raise invalid_authorization_type_error.to_exception()



async def verify_credentials(
        login: str,
        pwd: str,
        postgres: AsyncSession,
) -> PgUser:
    pg_user = await pg_get_user_by_username(login, postgres)

    if not pg_user:
        raise invalid_credentials_error.to_exception()

    pwd_is_valid = await verify_pwd_athread(pwd, pg_user.pwd_hash)

    if not pwd_is_valid:
        raise invalid_credentials_error.to_exception()

    return pg_user