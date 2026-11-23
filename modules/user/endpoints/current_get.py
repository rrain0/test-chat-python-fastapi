from fastapi import status, APIRouter

from core.postgres.init import AsyncPostgresDep
from modules.user.postgres.get_user_by_id import pg_get_user_by_id
from modules.session.app.provider.provide_app_session import ProvideAppSessionDep
from shared.backend.modules.user.api_model.user import BackApiUser
from shared.utils.fastapis.api_error_case import ApiErrorCase


router_user_current = APIRouter(prefix="/api/user/current")


responses = { }
no_user_by_id_error = ApiErrorCase(
    status_code=status.HTTP_400_BAD_REQUEST,
    error_code="NO_USER_BY_ID",
    error_msg="User with such id was not found",
).add_example_to_openapi_responses(responses)


@router_user_current.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=BackApiUser,
    responses=responses,
)
async def user_current_get(
        app_session: ProvideAppSessionDep,
        postgres: AsyncPostgresDep,
):
    pg_user = await pg_get_user_by_id(app_session.user_id, postgres)

    if not pg_user:
        raise no_user_by_id_error.to_exception()

    return pg_user
