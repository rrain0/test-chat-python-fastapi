from fastapi import Depends, status, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlmodel import Session
from db_connection.db_connection import get_session
from api_model.api_error import ApiError
from api_model.api_user import db_user_to_api_user, ApiUser
from api_model.api_user_create import ApiUserCreate
from db_model.db_user import DbUser
from db_repo.user_repo import user_by_login
from services.jwt_service import create_access_token
from services.pwd_hash_service import hash_password
from utils import datetimes

router = APIRouter(prefix="/user", tags=["User"])


# Эндпоинт регистрации пользователя
@router.post("/signup")
def user_signup(user_create: ApiUserCreate, session: Session = Depends(get_session)):

    # Проверяем, нет ли уже пользователя с таким логином
    existing_user_db = user_by_login(session, user_create.login)
    if existing_user_db:
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
    hashed_pwd = hash_password(user_create.pwd)

    # Создаем модель для БД (UUID сгенерируется автоматически через default_factory)
    db_user = DbUser(
        login=user_create.login,
        pwd_hash=hashed_pwd
    )

    # Сохраняем в PostgreSQL
    session.add(db_user)
    session.commit()

    # Обновляем текущий объект реальными данными из PostgreSQL
    session.refresh(db_user)

    access_token = create_access_token(
        user_id=db_user.id,
        created_at=datetimes.now()
    )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(
            UserSignup(
                access_token=access_token,
                user=db_user_to_api_user(db_user)
            )
        )
    )



class UserSignup(BaseModel):
    access_token: str
    user: ApiUser