from backend_api_model.back_api_user import BackApiUser
from db.model.db_user import DbUser


def back_api_user_from_db_user(db_user: DbUser) -> BackApiUser:
    return BackApiUser(
        id=db_user.id,
        login=db_user.login,
    )
