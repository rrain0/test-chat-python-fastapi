from fastapi import Request, FastAPI
from fastapi.exceptions import RequestValidationError

from core.api_errors.request_validation import create_request_validation_api_error_case


# Transforms pydantic validation error response


async def request_validation_error_handler(
        request: Request,
        ex: RequestValidationError,
):
    return create_request_validation_api_error_case(ex.errors()).to_json_response()



def setup_request_validation_error_handler(app: FastAPI):
    app.add_exception_handler(
        RequestValidationError,
        request_validation_error_handler
    )
