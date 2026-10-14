from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pygments.lexers import q
from sqlmodel import Session

from db_connection.db_connection import get_session
from db_model.db_tg_user import DbTgUser
from db_model.db_user import DbUser
from db_repo.tg_user_repo import db_upsert_tg_user, db_get_tg_user_by_id
from db_repo.user_repo import db_get_user_by_id
from services.jwt.jwt_tg_user_service import decode_tg_user_access_token
from services.jwt.jwt_user_service import decode_user_access_token



# Создаем схему безопасности
bearer_scheme = HTTPBearer()



def credentials_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Bearer"},
    )



def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        session: Session = Depends(get_session)
) -> DbUser:
    # credentials.scheme вернет строку "Bearer"
    # credentials.credentials вернет сам токен (строку)
    user_token_str = credentials.credentials
    # Decode token
    user_token = decode_user_access_token(user_token_str)
    # Query the user from Postgres using SQLModel
    db_user = db_get_user_by_id(session, user_token.user.id)
    if not db_user:
        raise credentials_exception()
    return db_user


def get_current_user_by_tg_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        session: Session = Depends(get_session)
) -> DbUser:
    tg_user_token_str = credentials.credentials
    tg_user_token = decode_tg_user_access_token(tg_user_token_str)

    tg_user = db_get_tg_user_by_id(session, tg_user_token.user_id)
    if not tg_user:
        raise credentials_exception()

    db_user = db_get_user_by_id(session, tg_user.user_id)
    assert db_user is not None

    return db_user


def get_current_tg_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        session: Session = Depends(get_session)
) -> DbTgUser:
    tg_token_str = credentials.credentials
    tg_token = decode_tg_user_access_token(tg_token_str)
    db_tg_user = DbTgUser(
        id=tg_token.user_id,
        username=tg_token.user_username,
        first_name=tg_token.user_first_name,
        last_name=tg_token.user_last_name,
    )
    db_upsert_tg_user(session, db_tg_user)
    return db_tg_user

