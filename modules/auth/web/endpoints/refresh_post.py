from fastapi import status, APIRouter, Request, Response
from redis_fastapi import AsyncRedisDep

from core.postgres.init import AsyncPostgresDep
from modules.session.unauthorized_error import unauthorized_error, unauthorized_exception
from modules.session.web.repo.refresh_web_session import commit_refresh_web_session
from modules.session.web.token_store.refresh_token import get_web_refresh_token, add_web_refresh_token
from shared.backend.modules.user.api_model.auth_web_refreshed import BackApiAuthWebRefreshed
from shared.utils.fastapis.get_client_ip import get_client_ip
from shared.utils.fastapis.get_client_user_agent_str import get_client_user_agent_str


router_auth_web_refresh = APIRouter(prefix="/api/auth/web/refresh")



responses = { }
unauthorized_error.add_example_to_openapi_responses(responses)


@router_auth_web_refresh.post(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=BackApiAuthWebRefreshed,
    responses=responses,
)
async def auth_web_refresh_post(
        request: Request,
        response: Response,
        postgres: AsyncPostgresDep,
        redis: AsyncRedisDep,
):
    refresh_token_str = get_web_refresh_token(request)
    if not refresh_token_str:
        raise unauthorized_exception()

    new_access_token_str, new_access_token, new_refresh_token_str, new_refresh_token = \
        await commit_refresh_web_session(
            refresh_token_str=refresh_token_str,
            user_ip=get_client_ip(request),
            user_agent_str=get_client_user_agent_str(request),
            postgres=postgres,
            redis=redis,
        )

    add_web_refresh_token(response, new_refresh_token_str, new_refresh_token.expires_at)
    return BackApiAuthWebRefreshed(
        access_token=new_access_token_str,
    )
