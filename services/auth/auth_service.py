from fastapi import HTTPException, status

from core.postgres.init import AsyncPostgresDep
from services.auth.bearer_auth_scheme import BearerAuthSchemeDep
from modules.user.postgres.user import PgUser
from modules.tg_user.db_repo.get_tg_user_by_id import get_tg_user_by_id
from modules.user.postgres.get_user_by_id import pg_get_user_by_id
from services.jwt.lib.jwt_tg_user_service import decode_tg_user_access_token




def credentials_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Bearer"},
    )





async def get_current_user_by_tg_user(
        credentials: BearerAuthSchemeDep,
        postgres: AsyncPostgresDep
) -> PgUser:
    tg_user_token_str = credentials.credentials

    try: tg_user_token = decode_tg_user_access_token(tg_user_token_str)
    except: raise credentials_exception()

    db_tg_user = await get_tg_user_by_id(postgres, tg_user_token.tg_user.id)
    if not db_tg_user:
        raise credentials_exception()

    pg_user = await pg_get_user_by_id(tg_user_token.user.id, postgres)
    if not pg_user:
        raise credentials_exception()

    if pg_user.id != db_tg_user.user_id:
        raise credentials_exception()

    return pg_user
