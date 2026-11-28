from core.api_error.utils import api_error_case_to_exception
from core.pwd_hash.pwd_hash import verify_pwd_athread
from modules.user.postgres.repo.get_by_username import pg_get_user_by_username
from modules.user.postgres.tables.user import PgUser
from shared.backend.modules.auth.api_errors.invalid_user_credentials import invalid_user_credentials_error_case
from shared.utils.postgres.async_postgres import AsyncPostgres


async def verify_user_credentials(
        login: str,
        pwd: str,
        postgres: AsyncPostgres,
) -> PgUser:
    pg_user = await pg_get_user_by_username(login, postgres)

    if not pg_user:
        raise api_error_case_to_exception(invalid_user_credentials_error_case)

    pwd_is_valid = await verify_pwd_athread(pwd, pg_user.pwd_hash)

    if not pwd_is_valid:
        raise api_error_case_to_exception(invalid_user_credentials_error_case)

    return pg_user
