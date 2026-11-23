from fastapi import status, APIRouter
from fastapi import Request, Response

from modules.session.web.repo.create_web_session import commit_create_web_session
from shared.backend.modules.user.api_model.user_logged_in import BackApiUserLoggedIn
from shared.backend.modules.user.api_model.user_to_login import BackApiUserToLogin
from core.postgres.init import AsyncPostgresDep
from modules.user.convert.db_user_to_back_api_user import db_user_to_back_api_user
from modules.session.web.token_store.refresh_token import add_web_refresh_token
from modules.user.postgres.get_user_by_username import pg_get_user_by_username
from modules.pwd_hash.pwd_hash import verify_pwd
from shared.utils.fastapis.api_error_case import ApiErrorCase
from shared.utils.fastapis.get_client_ip import get_client_ip
from shared.utils.fastapis.get_client_user_agent_str import get_client_user_agent_str
from redis_fastapi import AsyncRedisDep

router_user_login = APIRouter(prefix='/api/user/login')


responses = { }
invalid_credentials_error = ApiErrorCase(
    # Respond 400 instead of 401 because you don't need credentials to access this endpoint
    status_code=status.HTTP_400_BAD_REQUEST,
    error_code='INVALID_CREDENTIALS',
    error_msg='User with these login & password was not found',
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
    db_user = await pg_get_user_by_username(user_to_login.login, postgres)

    if not db_user:
        raise invalid_credentials_error.to_exception()

    pwd_is_valid = verify_pwd(user_to_login.pwd, db_user.pwd_hash)

    if not pwd_is_valid:
        raise invalid_credentials_error.to_exception()

    access_token_str, access_token, refresh_token_str, refresh_token = \
        await commit_create_web_session(
            user_id=db_user.id,
            user_username=db_user.username,
            user_ip=get_client_ip(request),
            user_agent_str=get_client_user_agent_str(request),
            postgres=postgres,
            redis=redis,
        )

    add_web_refresh_token(response, refresh_token_str, refresh_token.expires_at)
    return BackApiUserLoggedIn(
        access_token=access_token_str,
        user=db_user_to_back_api_user(db_user)
    )

