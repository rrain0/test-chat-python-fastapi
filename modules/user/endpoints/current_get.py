from fastapi import status, APIRouter

from core.postgres.setup import AsyncPostgresDep
from modules.auth.api_errors.unauthorized_user_utils import unauthorized_user_exception
from modules.user.mappers.pg_to_back_api_user import pg_to_back_api_user
from modules.user.postgres.repo.get_by_id import pg_get_user_by_id
from modules.auth.provider.provide_user_session import ProvideAppSessionDep
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
    pg_user = await pg_get_user_by_id(app_session.user_id, postgres)

    # User can be deleted between checking session and retrieving full user
    if not pg_user:
        raise unauthorized_user_exception()

    return pg_to_back_api_user(pg_user)
