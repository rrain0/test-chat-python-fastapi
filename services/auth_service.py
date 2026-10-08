from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session

from db_connection.db_connection import get_session
from db_model.db_user import DbUser
from db_repo.user_repo import user_by_id
from services.jwt_service import decode_access_token



# Создаем схему безопасности
bearer_scheme = HTTPBearer()



def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        session: Session = Depends(get_session)
) -> DbUser:
    # credentials.scheme вернет строку "Bearer"
    # credentials.credentials вернет сам токен (строку)
    token = credentials.credentials
    # Decode token
    tk = decode_access_token(token)
    # Query the user from Postgres using SQLModel
    db_user = user_by_id(session, tk.user_id)
    if not db_user:
        raise credentials_exception()
    return db_user
    try:
        # Decode token
        tk = decode_access_token(token)
        # Query the user from Postgres using SQLModel
        db_user = user_by_id(session, tk.user_id)
        if not db_user:
            raise credentials_exception()
        return db_user

    except:
        raise credentials_exception()




def credentials_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="COULD_NOT_VALIDATE_CREDENTIALS",
        headers={"WWW-Authenticate": "Bearer"},
    )
