from fastapi import status, APIRouter

from core.postgres.setup import AsyncPostgresDep
from modules.user.postgres.repo.get_by_id import pg_get_user_by_id
from modules.auth.provider.provide_app_session import ProvideAppSessionDep
from modules.user.postgres.tables.user import PgUser
from shared.backend.modules.user.api_model.user import BackApiUser


router_user_current_get = APIRouter(prefix="/api/user/current")


@router_user_current_get.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=BackApiUser,
)
async def user_current_get(
        app_session: ProvideAppSessionDep,
        postgres: AsyncPostgresDep,
):
    pg_user: PgUser = await pg_get_user_by_id(app_session.user_id, postgres)
    return pg_user
