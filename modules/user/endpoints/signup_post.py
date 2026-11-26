from uuid import uuid7

from fastapi import status, APIRouter
from fastapi import Request, Response
from pydantic_core import PydanticCustomError
from redis_fastapi import AsyncRedisDep

from core.api_error.utils import add_api_error_case_to_openapi_responses_example
from modules.user.api_errors.username_exists import username_exists_error_case
from modules.user.postgres.repo.exists_by_username import pg_user_exists_by_username
from modules.session_web.actions.create import commit_create_web_session
from shared.backend.modules.user.api_model.logged_in import BackApiUserLoggedIn
from shared.backend.modules.user.api_model.to_signup import BackApiUserToSignup
from core.postgres.setup import AsyncPostgresDep
from modules.user.mappers.pg_to_back_api_user import pg_user_to_back_api_user
from modules.session_web.token_store.refresh_token import add_web_refresh_token
from modules.user.postgres.tables.user import PgUser
from core.pwd_hash.pwd_hash import hash_pwd_athread
from pydantic import field_validator

from shared.utils.fastapis.get_client_ip import get_client_ip
from shared.utils.fastapis.get_client_user_agent_str import get_client_user_agent_str
from shared.backend.modules.user.validators.user_to_signup_pwd import validate_user_to_signup_pwd
from shared.backend.modules.user.validators.user_to_signup_username import validate_user_to_signup_username


router_user_signup_post = APIRouter(prefix="/api/user/signup")


responses = { }
add_api_error_case_to_openapi_responses_example(username_exists_error_case, responses)


class BackApiUserToSignupWithValidation(BackApiUserToSignup):
    @field_validator("username", mode="after")
    @classmethod
    def validate_username_field(cls, v: str) -> str:
        try:
            validate_user_to_signup_username(v)
        except ValueError as ex:
            raise PydanticCustomError("invalid_username", str(ex))
        return v

    @field_validator("pwd", mode="after")
    @classmethod
    def validate_pwd_field(cls, v: str) -> str:
        try:
            validate_user_to_signup_pwd(v)
        except ValueError as ex:
            raise PydanticCustomError("invalid_password", str(ex))
        return v


@router_user_signup_post.post(
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
    pg_user_exists = await pg_user_exists_by_username(user_to_signup.username, postgres)
    if pg_user_exists:
        raise username_exists_error_case.to_exception()

    # Hash the password
    hashed_pwd = await hash_pwd_athread(user_to_signup.pwd)

    # Create database model instance
    pg_user = PgUser(
        id=uuid7(),
        username=user_to_signup.username,
        pwd_hash=hashed_pwd,
    )

    # Save into FastAPI
    postgres.add(pg_user)
    # Save into Postgres transaction
    await postgres.flush()

    # Create user session and save into Postgres permanently
    (
        access_token_str,
        access_token,
        refresh_token_str,
        refresh_token,
    ) = await commit_create_web_session(
        user_id=pg_user.id,
        user_username=pg_user.username,
        user_ip=get_client_ip(request),
        user_agent_str=get_client_user_agent_str(request),
        postgres=postgres,
        redis=redis,
    )

    # Add refresh token to response as a cookie
    add_web_refresh_token(response, refresh_token_str, refresh_token.expires_at)
    return BackApiUserLoggedIn(
        access_token=access_token_str,
        user=pg_user_to_back_api_user(pg_user)
    )
