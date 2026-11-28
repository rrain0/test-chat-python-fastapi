from shared.backend.core.api_error.api_error_case import ApiErrorCase


# Respond 400 instead of 401 because you don't need credentials to access this endpoint
invalid_user_credentials_error_case = ApiErrorCase(
    status_code=400, # HTTP 400 Bad Request
    error_code="INVALID_USER_CREDENTIALS",
    error_msg="User with these login & password was not found",
)
