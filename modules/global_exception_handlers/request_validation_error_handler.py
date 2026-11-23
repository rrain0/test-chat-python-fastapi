from typing import Any

from fastapi import Request, status, FastAPI
from fastapi.exceptions import RequestValidationError

from shared.utils.fastapis.api_error_case import ApiErrorCase



# Transforms pydantic validation error response

def create_request_validation_api_error_case(error_detail: Any = None):
    return ApiErrorCase(
        status_code=status.HTTP_400_BAD_REQUEST,
        error_code='DATA_FORMAT_ERROR',
        error_msg='Invalid input data format',
        error_detail=error_detail,
    )



async def request_validation_error_handler(
        request: Request,
        ex: RequestValidationError,
):
    return create_request_validation_api_error_case(ex.errors()).to_json_response()



def register_request_validation_error_handler(app: FastAPI):
    app.add_exception_handler(
        RequestValidationError,
        request_validation_error_handler
    )
