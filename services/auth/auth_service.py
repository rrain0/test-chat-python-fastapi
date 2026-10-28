from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pygments.lexers import q
from sqlmodel import Session

from db.setup.db_setup import get_session
from db.tables.db_user import DbUser
from db.repo.tg_user_repo import db_upsert_tg_user, db_get_tg_user_by_id
from db.repo.user_repo import db_get_user_by_id
from services.jwt.lib.jwt_tg_user_service import decode_tg_user_access_token
from services.jwt.lib.jwt_user_service import decode_user_access_token



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
    try: user_token = decode_user_access_token(user_token_str)
    except: raise credentials_exception()
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

    try: tg_user_token = decode_tg_user_access_token(tg_user_token_str)
    except: raise credentials_exception()

    db_tg_user = db_get_tg_user_by_id(session, tg_user_token.tg_user.id)
    if not db_tg_user:
        raise credentials_exception()

    db_user = db_get_user_by_id(session, tg_user_token.user.id)
    if not db_user:
        raise credentials_exception()

    if db_user.id != db_tg_user.user_id:
        raise credentials_exception()

    return db_user
