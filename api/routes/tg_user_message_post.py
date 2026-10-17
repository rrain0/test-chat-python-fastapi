from fastapi import Depends, status, APIRouter
from sqlmodel import Session

from db.connection.db_connection import get_session
from db.model.db_tg_user import DbTgUser
from services.auth.auth_service import get_current_tg_user

tg_user_message_router = APIRouter(prefix="/tg_user/message")



@tg_user_message_router.post("", status_code=status.HTTP_200_OK, response_model=None)
def tg_user_message_post_route_handler(
        db_tg_user: DbTgUser = Depends(get_current_tg_user),
        session: Session = Depends(get_session)
):
    print("TG_USERRRRRR", db_tg_user.username)