from fastapi import Request, FastAPI

from shared.utils.fastapis.api_error_case import ApiErrorCaseException


async def api_error_case_exception_handler(
        request: Request,
        ex: ApiErrorCaseException,
):
    return ex.api_error_case.to_json_response()



def register_api_error_case_exception_handler(app: FastAPI):
    app.add_exception_handler(
        ApiErrorCaseException,
        api_error_case_exception_handler
    )
