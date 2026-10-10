from fastapi import Depends, status, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlmodel import Session
from db_connection.db_connection import get_session
from api_model.api_error import ApiError
from api_model.api_user import db_user_to_api_user, ApiUser
from db_model.db_user import DbUser
from db_repo.user_repo import user_by_login
from services.jwt_user_service import create_user_access_token
from services.pwd_hash_service import hash_password
from utils import datetimes
from pydantic import BaseModel, model_validator
from utils.validators import validate_user_signup_login, validate_user_signup_password



user_signup_router = APIRouter(prefix="/user/signup")



class ApiUserSignup(BaseModel):
    login: str
    pwd: str

    @model_validator(mode="after")
    def validate_after(self) -> "ApiUserSignup":
        validate_user_signup_login(self.login)
        validate_user_signup_password(self.pwd)
        return self

class ApiUserSignedUp(BaseModel):
    access_token: str
    user: ApiUser



@user_signup_router.post("", status_code=status.HTTP_201_CREATED, response_model=ApiUserSignedUp)
def user_signup_route_handler(api_user_signup: ApiUserSignup, session: Session = Depends(get_session)):

    # Проверяем, нет ли уже пользователя с таким логином
    db_user = user_by_login(session, api_user_signup.login)
    if db_user:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(
                ApiError(
                    error_code="LOGIN_EXISTS",
                    msg="Пользователь с таким логином уже существует",
                )
            )
        )

    # Хэшируем пароль
    hashed_pwd = hash_password(api_user_signup.pwd)

    # Создаем модель для БД (UUID сгенерируется автоматически через default_factory)
    db_user = DbUser(
        login=api_user_signup.login,
        pwd_hash=hashed_pwd
    )

    # Сохраняем в PostgreSQL
    session.add(db_user)
    session.commit()

    # Обновляем текущий объект реальными данными из PostgreSQL
    session.refresh(db_user)

    access_token = create_user_access_token(
        user_id=db_user.id,
        created_at=datetimes.now()
    )

    return ApiUserSignedUp(
        access_token=access_token,
        user=db_user_to_api_user(db_user)
    )

