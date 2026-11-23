from fastapi import status, APIRouter

from core.postgres.init import AsyncPostgresDep
from modules.user.postgres.get_user_by_id import pg_get_user_by_id
from modules.session.app.provider.provide_app_session import ProvideAppSessionDep
from shared.backend.modules.msg.api_model.msg_text import BackApiMsgText
from shared.backend.modules.user.api_model.user import BackApiUser
from shared.utils.fastapis.api_error_case import ApiErrorCase


router_msg = APIRouter(prefix="/api/msg")


responses = { }



@router_msg.post(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=None,
    responses=responses,
)
async def msg_post(
        msg_text: BackApiMsgText,
        app_session: ProvideAppSessionDep,
        postgres: AsyncPostgresDep,
):
    print("MSG_POST", msg_text)

    return None
