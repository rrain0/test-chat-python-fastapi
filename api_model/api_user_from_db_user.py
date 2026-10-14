from api_model.api_user import ApiUser
from db_model.db_user import DbUser



def api_user_from_db_user(db_user: DbUser) -> ApiUser:
    return ApiUser(
        id=db_user.id,
        login=db_user.login,
    )
