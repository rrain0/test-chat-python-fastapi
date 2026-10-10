from fastapi import Depends, status, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlmodel import Session

from db_connection.db_connection import get_session
from api_model.api_error import ApiError
from api_model.api_user import db_user_to_api_user, ApiUser
from db_model.db_tg_user import DbTgUser
from db_repo.user_repo import user_by_login
from services.auth_service import get_current_tg_user
from services.jwt_user_service import create_user_access_token
from services.pwd_hash_service import verify_password
from utils import datetimes



tg_user_post_message_router = APIRouter(prefix="/tg_user/message")



@tg_user_post_message_router.post("", status_code=status.HTTP_200_OK, response_model=None)
def tg_user_post_message_route_handler(
        db_tg_user: DbTgUser = Depends(get_current_tg_user),
        session: Session = Depends(get_session)
):
    print("TG_USERRRRRR", db_tg_user.username)