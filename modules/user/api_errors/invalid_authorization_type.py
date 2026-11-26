from starlette import status

from shared.backend.core.api_error.case import ApiErrorCase


# Respond 400 instead of 401 because you don't need credentials to access this endpoint
invalid_authorization_type_error_case = ApiErrorCase(
    status_code=status.HTTP_400_BAD_REQUEST,
    error_code="INVALID_AUTHORIZATION_TYPE",
    error_msg="Authorization header does not match any valid authorization type",
)
