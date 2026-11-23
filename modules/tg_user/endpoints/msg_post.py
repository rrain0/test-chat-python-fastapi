from fastapi import Depends, status, APIRouter
from pydantic import BaseModel

from core.postgres.init import AsyncPostgresDep
from modules.msg.postgres.msg import DbMsg
from modules.user.postgres.user import PgUser
from modules.chat.db_repo.upsert_chat_of_single_user import upsert_chat_of_single_user
from services.auth.auth_service import get_current_user_by_tg_user
from shared.utils.datetimes.now import now

router_tg_user_msg = APIRouter(prefix="/api/tg_user/msg")



class MsgText(BaseModel):
    msg_text: str

@router_tg_user_msg.post("", status_code=status.HTTP_200_OK, response_model=None)
async def tg_user_msg_post(
        msg_text: MsgText,
        postgres: AsyncPostgresDep,
        db_user: PgUser = Depends(get_current_user_by_tg_user),
):
    chat = await upsert_chat_of_single_user(postgres, db_user.id)

    msg = DbMsg(
        chat_id=chat.id,
        sent_at=now(),
        text_content=msg_text.msg_text,
    )
    postgres.add(msg)
    await postgres.commit()
    await postgres.refresh(msg)
