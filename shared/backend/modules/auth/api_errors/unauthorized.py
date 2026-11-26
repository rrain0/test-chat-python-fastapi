from shared.backend.core.api_error.case import ApiErrorCase


unauthorized_error_case = ApiErrorCase(
    status_code=401, # HTTP 401 UNAUTHORIZED
    error_code="UNAUTHORIZED",
)
