from fastapi import Request, FastAPI

from core.api_error.exception import ApiErrorCaseException
from core.api_error.utils import api_error_case_to_json_response


async def api_error_case_exception_handler(
        request: Request,
        ex: ApiErrorCaseException,
):
    return api_error_case_to_json_response(ex.api_error_case)



def setup_api_error_case_exception_handler(app: FastAPI):
    app.add_exception_handler(
        ApiErrorCaseException,
        api_error_case_exception_handler
    )
