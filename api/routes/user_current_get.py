from fastapi import Depends, status, APIRouter

from backend_api_model.back_api_user import BackApiUser
from api.convert.back_api_user_from_db_user import back_api_user_from_db_user
from db.tables.db_user import DbUser
from services.auth.auth_service import get_current_user



user_current_router = APIRouter(prefix="/user/current")



@user_current_router.get("", status_code=status.HTTP_200_OK, response_model=BackApiUser)
def user_current_get_route_handler(db_user: DbUser = Depends(get_current_user)):
    return back_api_user_from_db_user(db_user)
