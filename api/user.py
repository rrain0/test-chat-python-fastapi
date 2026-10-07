from fastapi import Depends, HTTPException, status, APIRouter
from sqlmodel import Session, select
from db_connection import get_session
from model_api.ApiError import ApiError
from model_api.User import User
from model_api.UserCreate import UserCreate
from model_db.UserDb import UserDb
from services.hash_pwd import hash_password


router = APIRouter(prefix="/user", tags=["User"])


# Эндпоинт регистрации пользователя
@router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
def user_signup(user_create: UserCreate, session: Session = Depends(get_session)):

    # Проверяем формат ввода
    user_create_format_error = user_create.validate_after()
    if user_create_format_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=user_create_format_error.model_dump()
        )

    # Проверяем, нет ли уже пользователя с таким логином
    existing_user_db = session.exec(select(UserDb).where(UserDb.login == user_create.login)).first()
    if existing_user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ApiError(
                error_code="LOGIN_EXISTS",
                description="Пользователь с таким логином уже существует",
            ).model_dump()
        )

    # Хэшируем пароль
    hashed_pwd = hash_password(user_create.pwd)

    # Создаем модель для БД (UUID сгенерируется автоматически через default_factory)
    user_db = UserDb(
        login=user_create.login,
        pwd_hash=hashed_pwd
    )

    # Сохраняем в PostgreSQL
    session.add(user_db)
    session.commit()

    # Обновить данными из PostgreSQL
    session.refresh(user_db)

    return user_db