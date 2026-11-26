from fastapi import status, APIRouter
from fastapi import Request, Response

from core.api_error.utils import add_api_error_case_to_openapi_responses_example
from modules.session.tg_bot.token_store.access_token import get_tg_bot_access_token
from modules.session.web.actions.create import commit_create_web_session
from modules.user.api_errors.invalid_authorization_type import invalid_authorization_type_error_case
from modules.user.api_errors.invalid_credentials import invalid_credentials_error_case
from modules.user.postgres.tables.user import PgUser
from shared.backend.modules.user.api_model.logged_in import BackApiUserLoggedIn
from shared.backend.modules.user.api_model.to_login import BackApiUserToLogin
from core.postgres.setup import AsyncPostgresDep
from modules.user.mappers.pg_to_back_api_user import pg_user_to_back_api_user
from modules.session.web.token_store.refresh_token import add_web_refresh_token
from modules.user.postgres.repo.get_by_username import pg_get_user_by_username
from core.pwd_hash.pwd_hash import verify_pwd_athread
from shared.utils.fastapis.get_client_ip import get_client_ip
from shared.utils.fastapis.get_client_user_agent_str import get_client_user_agent_str
from redis_fastapi import AsyncRedisDep

from shared.utils.fastapis.auth_header_not_exists import auth_header_not_exists
from shared.utils.postgres.async_postgres import AsyncPostgres


router_user_login_post = APIRouter(prefix="/api/user/login")


responses = { }
add_api_error_case_to_openapi_responses_example(invalid_authorization_type_error_case, responses)
add_api_error_case_to_openapi_responses_example(invalid_credentials_error_case, responses)


@router_user_login_post.post(
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

        (
            access_token_str,
            access_token,
            refresh_token_str,
            refresh_token,
        ) = await commit_create_web_session(
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


    raise invalid_authorization_type_error_case.to_exception()



async def verify_credentials(
        login: str,
        pwd: str,
        postgres: AsyncPostgres,
) -> PgUser:
    pg_user = await pg_get_user_by_username(login, postgres)

    if not pg_user:
        raise invalid_credentials_error_case.to_exception()

    pwd_is_valid = await verify_pwd_athread(pwd, pg_user.pwd_hash)

    if not pwd_is_valid:
        raise invalid_credentials_error_case.to_exception()

    return pg_user