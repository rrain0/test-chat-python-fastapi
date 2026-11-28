from fastapi import status, APIRouter
from fastapi import Request

from core.api_error.utils import api_error_cases_add_to_openapi_responses_examples, api_error_case_to_exception
from modules.session_tg_bot.actions.create import commit_create_tg_bot_session
from modules.session_tg_bot.jwt_access.decode import decode_tg_bot_access_token
from modules.session_tg_bot.token_store.access_token import get_tg_bot_access_token
from modules.user.actions.verify_user_credentials import verify_user_credentials
from modules.user.mappers.pg_to_back_api_user import pg_to_back_api_user
from shared.backend.modules.auth.api_errors.invalid_user_credentials import invalid_user_credentials_error_case
from core.postgres.setup import AsyncPostgresDep
from redis_fastapi import AsyncRedisDep

from shared.backend.modules.auth.api_errors.unauthorized_service import unauthorized_service_error_case
from shared.backend.modules.auth_tg_bot.api_model.logged_in import BackApiTgBotUserLoggedIn
from shared.backend.modules.auth_tg_bot.api_model.to_login import BackApiTgBotUserToLogin


router_auth_tg_bot_login_post = APIRouter(prefix="/api/auth/tg-bot/login")


@router_auth_tg_bot_login_post.post(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=BackApiTgBotUserLoggedIn,
    responses=api_error_cases_add_to_openapi_responses_examples(
        unauthorized_service_error_case,
        invalid_user_credentials_error_case,
    ),
)
async def auth_tg_bot_login_post(
        user_to_login: BackApiTgBotUserToLogin,
        request: Request,
        postgres: AsyncPostgresDep,
        redis: AsyncRedisDep,
):
    tg_bot_access_token_str = get_tg_bot_access_token(request)
    if not tg_bot_access_token_str:
        raise api_error_case_to_exception(unauthorized_service_error_case)

    try: tg_bot_access_token = decode_tg_bot_access_token(tg_bot_access_token_str)
    except:
        raise api_error_case_to_exception(unauthorized_service_error_case)

    pg_user = await verify_user_credentials(user_to_login.login, user_to_login.pwd, postgres)

    await commit_create_tg_bot_session(
        user_id=pg_user.id,
        tg_user_id=tg_bot_access_token.tg_user_id,
        postgres=postgres,
        redis=redis,
    )

    return BackApiTgBotUserLoggedIn(
        user=pg_to_back_api_user(pg_user)
    )
