from fastapi import status, APIRouter, Response
from redis_fastapi import AsyncRedisDep

from core.postgres.setup import AsyncPostgresDep
from modules.session.web.token_store.refresh_token import delete_web_refresh_token
from modules.session.web.actions.remove import commit_remove_web_session
from modules.session.app.provider.provide import ProvideAppSessionDep


router_user_logout_post = APIRouter(prefix="/api/user/logout")


@router_user_logout_post.post(
    path="",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def user_logout(
        app_session: ProvideAppSessionDep,
        response: Response,
        postgres: AsyncPostgresDep,
        redis: AsyncRedisDep,
):
    await commit_remove_web_session(
        user_id=app_session.user_id,
        session_id=app_session.session_id,
        postgres=postgres,
        redis=redis,
    )
    delete_web_refresh_token(response)


