from typing import Any

from fastapi import status

from shared.backend.core.api_error.api_error_case import ApiErrorCase


def create_request_validation_api_error_case(error_detail: Any = None):
    return ApiErrorCase(
        status_code=status.HTTP_400_BAD_REQUEST,
        error_code="DATA_FORMAT_ERROR",
        error_msg="Invalid input data format",
        error_detail=error_detail,
    )
