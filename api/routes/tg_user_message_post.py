from fastapi import Depends, status, APIRouter
from pydantic import BaseModel
from sqlmodel import Session

from db.connection.db_connection import get_session
from db.model.db_user import DbUser
from services.auth.auth_service import get_current_user_by_tg_user

tg_user_message_router = APIRouter(prefix="/tg_user/message")



class MessageText(BaseModel):
    message_text: str

@tg_user_message_router.post("", status_code=status.HTTP_200_OK, response_model=None)
def tg_user_message_post_route_handler(
        message_text: MessageText,
        db_user: DbUser = Depends(get_current_user_by_tg_user),
        session: Session = Depends(get_session)
):
    print("USER_LOGIN", db_user.login)
    print("MESSAGE_TEXT", message_text.message_text)
