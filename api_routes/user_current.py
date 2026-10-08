from fastapi import Depends, status, APIRouter

from api_model.api_user import db_user_to_api_user, ApiUser
from db_model.db_user import DbUser
from services.auth_service import get_current_user



user_current_router = APIRouter(prefix="/user/current")



@user_current_router.get("", status_code=status.HTTP_200_OK, response_model=ApiUser)
def user_current_route_handler(db_user: DbUser = Depends(get_current_user)):
    return db_user_to_api_user(db_user)
