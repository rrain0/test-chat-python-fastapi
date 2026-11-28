from shared.backend.core.api_error.api_error_case import ApiErrorCase


unauthorized_service_error_case = ApiErrorCase(
    status_code=401, # HTTP 401 UNAUTHORIZED
    error_code="UNAUTHORIZED_SERVICE",
)
