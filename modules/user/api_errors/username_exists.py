from starlette import status

from shared.backend.core.api_error.case import ApiErrorCase

username_exists_error_case = ApiErrorCase(
    status_code=status.HTTP_400_BAD_REQUEST,
    error_code="USERNAME_EXISTS",
    error_msg="User with this username already exists",
)
