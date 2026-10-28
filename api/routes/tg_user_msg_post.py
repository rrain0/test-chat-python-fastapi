from fastapi import Depends, status, APIRouter
from pydantic import BaseModel
from sqlmodel import Session

from db.setup.db_setup import get_session
from db.tables.db_msg import DbMsg
from db.tables.db_user import DbUser
from db.repo.chat_repo import upsert_chat_of_single_user
from services.auth.auth_service import get_current_user_by_tg_user
from utils.datetimes import now

tg_user_msg_router = APIRouter(prefix="/tg_user/msg")



class MsgText(BaseModel):
    msg_text: str

@tg_user_msg_router.post("", status_code=status.HTTP_200_OK, response_model=None)
def tg_user_msg_post_route_handler(
        msg_text: MsgText,
        db_user: DbUser = Depends(get_current_user_by_tg_user),
        session: Session = Depends(get_session)
):
    chat = upsert_chat_of_single_user(session, db_user.id)

    msg = DbMsg(
        chat_id=chat.id,
        sent_at=now(),
        text_content=msg_text.msg_text,
    )
    session.add(msg)
    session.commit()
    session.refresh(msg)

    #print("USER_LOGIN", db_user.login)
    #print("MSG_TEXT", msg_text.msg_text)
    #print("MSG_SAVED", msg)
