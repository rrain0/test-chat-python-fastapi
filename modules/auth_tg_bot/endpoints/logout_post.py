from fastapi import status, APIRouter, Response
from redis_fastapi import AsyncRedisDep

from core.postgres.setup import AsyncPostgresDep
from modules.auth.provider.provide_user_session import ProvideAppSessionDep


router_auth_tg_bot_logout_post = APIRouter(prefix="/api/auth/tg-bot/logout")


@router_auth_tg_bot_logout_post.post(
    path="",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def auth_tg_bot_logout(
        app_session: ProvideAppSessionDep,
        response: Response,
        postgres: AsyncPostgresDep,
        redis: AsyncRedisDep,
):
    raise NotImplementedError


