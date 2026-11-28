from fastapi import status, APIRouter
from fastapi import Request, Response

from core.api_error.utils import api_error_cases_add_to_openapi_responses_examples
from modules.user.actions.verify_user_credentials import verify_user_credentials
from modules.session_web.actions.create import commit_create_web_session
from shared.backend.modules.auth.api_errors.invalid_user_credentials import invalid_user_credentials_error_case
from shared.backend.modules.auth_web.api_model.logged_in import BackApiWebUserLoggedIn
from shared.backend.modules.auth_web.api_model.to_login import BackApiWebUserToLogin
from core.postgres.setup import AsyncPostgresDep
from modules.user.mappers.pg_to_back_api_user import pg_to_back_api_user
from modules.session_web.token_store.refresh_token import add_web_refresh_token
from shared.utils.fastapis.get_client_ip import get_client_ip
from shared.utils.fastapis.get_client_user_agent_str import get_client_user_agent_str
from redis_fastapi import AsyncRedisDep

router_auth_web_login_post = APIRouter(prefix="/api/auth/web/login")


@router_auth_web_login_post.post(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=BackApiWebUserLoggedIn,
    responses=api_error_cases_add_to_openapi_responses_examples(
        invalid_user_credentials_error_case,
    ),
)
async def auth_web_login_post(
        user_to_login: BackApiWebUserToLogin,
        request: Request,
        response: Response,
        postgres: AsyncPostgresDep,
        redis: AsyncRedisDep,
):
    pg_user = await verify_user_credentials(user_to_login.login, user_to_login.pwd, postgres)

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
    return BackApiWebUserLoggedIn(
        access_token=access_token_str,
        user=pg_to_back_api_user(pg_user)
    )
