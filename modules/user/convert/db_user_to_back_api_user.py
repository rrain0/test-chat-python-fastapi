from shared.backend.modules.user.api_model.user import BackApiUser
from modules.user.postgres.user import PgUser


def db_user_to_back_api_user(db_user: PgUser) -> BackApiUser:
    return BackApiUser(
        id=db_user.id,
        username=db_user.username,
    )
