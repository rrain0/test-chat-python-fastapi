from shared.backend.modules.user.api_model.user import BackApiUser
from modules.user.postgres.tables.user import PgUser


def pg_user_to_back_api_user(pg_user: PgUser) -> BackApiUser:
    return BackApiUser(
        id=pg_user.id,
        username=pg_user.username,
    )
