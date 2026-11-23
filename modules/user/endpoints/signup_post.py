from uuid import uuid7

from fastapi import status, APIRouter
from fastapi import Request, Response
from pydantic_core import PydanticCustomError
from redis_fastapi import AsyncRedisDep

from modules.user.postgres.user_exists_by_username import pg_user_exists_by_username
from modules.session.web.repo.create_web_session import commit_create_web_session
from shared.backend.modules.user.api_model.user_logged_in import BackApiUserLoggedIn
from shared.backend.modules.user.api_model.user_to_signup import BackApiUserToSignup
from core.postgres.init import AsyncPostgresDep
from modules.user.convert.db_user_to_back_api_user import db_user_to_back_api_user
from modules.session.web.token_store.refresh_token import add_web_refresh_token
from modules.user.postgres.user import PgUser
from modules.pwd_hash.pwd_hash import hash_pwd
from pydantic import field_validator

from shared.utils.fastapis.api_error_case import ApiErrorCase
from shared.utils.fastapis.get_client_ip import get_client_ip
from shared.utils.fastapis.get_client_user_agent_str import get_client_user_agent_str
from shared.backend.modules.validators.user_to_signup_pwd import validate_user_to_signup_pwd
from shared.backend.modules.validators.user_to_signup_username import validate_user_to_signup_username


router_user_signup = APIRouter(prefix='/api/user/signup')


responses = { }
username_exists_error = ApiErrorCase(
    status_code=status.HTTP_400_BAD_REQUEST,
    error_code='USERNAME_EXISTS',
    error_msg='User with this username already exists',
).add_example_to_openapi_responses(responses)


class BackApiUserToSignupWithValidation(BackApiUserToSignup):
    @field_validator('username', mode='after')
    @classmethod
    def validate_username_field(cls, v: str) -> str:
        try:
            validate_user_to_signup_username(v)
        except ValueError as ex:
            raise PydanticCustomError(
                'invalid_username',  # Рекомендуется писать code в snake_case без пробелов
                str(ex),
            )
        return v

    @field_validator('pwd', mode='after')
    @classmethod
    def validate_pwd_field(cls, v: str) -> str:
        try:
            validate_user_to_signup_pwd(v)
        except ValueError as ex:
            raise PydanticCustomError(
                'invalid_password',
                str(ex),
            )
        return v


@router_user_signup.post(
    path="", 
    status_code=status.HTTP_201_CREATED, 
    response_model=BackApiUserLoggedIn,
    responses=responses,
)
async def user_signup_post(
        user_to_signup: BackApiUserToSignupWithValidation,
        request: Request,
        response: Response,
        postgres: AsyncPostgresDep,
        redis: AsyncRedisDep,
):
    # Check whether user with this username already exists
    db_user_exists = await pg_user_exists_by_username(user_to_signup.username, postgres)
    if db_user_exists:
        raise username_exists_error.to_exception()

    # Hash the password
    hashed_pwd = hash_pwd(user_to_signup.pwd)

    # Create database model instance
    db_user = PgUser(
        id=uuid7(),
        username=user_to_signup.username,
        pwd_hash=hashed_pwd,
    )

    # Save into FastAPI
    postgres.add(db_user)
    # Save into Postgres transaction
    await postgres.flush()

    # Create user session and save into Postgres permanently
    access_token_str, access_token, refresh_token_str, refresh_token \
        = await commit_create_web_session(
            user_id=db_user.id,
            user_username=db_user.username,
            user_ip=get_client_ip(request),
            user_agent_str=get_client_user_agent_str(request),
            postgres=postgres,
            redis=redis,
        )

    # Add refresh token to response as a cookie
    add_web_refresh_token(response, refresh_token_str, refresh_token.expires_at)
    return BackApiUserLoggedIn(
        access_token=access_token_str,
        user=db_user_to_back_api_user(db_user)
    )
