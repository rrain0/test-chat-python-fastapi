from fastapi import status, APIRouter

from core.postgres.setup import AsyncPostgresDep
from modules.session.app.provider.provide import ProvideAppSessionDep
from shared.backend.modules.msg.api_model.msg_text import BackApiMsgText


router_msg_post = APIRouter(prefix="/api/msg")


responses = { }



@router_msg_post.post(
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
