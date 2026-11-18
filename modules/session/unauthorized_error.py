from fastapi import status

from shared.utils.fastapis.api_error.api_error_case import ApiErrorCase


unauthorized_error = ApiErrorCase(
    status_code=status.HTTP_401_UNAUTHORIZED,
    error_code='UNAUTHORIZED',
)

def unauthorized_exception():
    return unauthorized_error.to_exception()
