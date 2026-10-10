from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from pygments.lexers import q
from sqlmodel import Session

from db_connection.db_connection import get_session
from db_model.db_tg_user import DbTgUser
from db_model.db_user import DbUser
from db_repo.tg_user_repo import upsert_tg_user
from db_repo.user_repo import user_by_id
from services.jwt_tg_user_service import decode_tg_user_access_token
from services.jwt_user_service import decode_user_access_token



# Создаем схему безопасности
bearer_scheme = HTTPBearer()



def credentials_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="COULD_NOT_VALIDATE_CREDENTIALS",
        headers={"WWW-Authenticate": "Bearer"},
    )



def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        session: Session = Depends(get_session)
) -> DbUser:
    # credentials.scheme вернет строку "Bearer"
    # credentials.credentials вернет сам токен (строку)
    token_str = credentials.credentials
    # Decode token
    token = decode_user_access_token(token_str)
    # Query the user from Postgres using SQLModel
    db_user = user_by_id(session, token.user_id)
    if not db_user:
        raise credentials_exception()
    return db_user


def get_current_tg_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        session: Session = Depends(get_session)
) -> DbTgUser:
    token_str = credentials.credentials
    token = decode_tg_user_access_token(token_str)
    db_tg_user = DbTgUser(
        id=token.user_id,
        username=token.user_username,
        first_name=token.user_first_name,
        last_name=token.user_last_name,
    )
    upsert_tg_user(session, db_tg_user)
    return db_tg_user

