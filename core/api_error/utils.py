from core.api_error.back_api_error import BackApiError
from shared.backend.core.api_error.case import ApiErrorCase
from core.api_error.exception import ApiErrorCaseException
from fastapi.responses import JSONResponse


def api_error_case_to_back_api_error(api_error_case: ApiErrorCase) -> BackApiError:
    return BackApiError(
        error_code=api_error_case.error_code,
        error_msg=api_error_case.error_msg,
        error_detail=api_error_case.error_detail,
    )



def api_error_case_to_exception(api_error_case: ApiErrorCase) -> ApiErrorCaseException:
    return ApiErrorCaseException(api_error_case)



def api_error_case_to_json_response(api_error_case: ApiErrorCase):
    return JSONResponse(
        status_code=api_error_case.status_code,
        content=api_error_case_to_back_api_error(api_error_case).model_dump(mode="json"),
    )


def add_api_error_case_to_openapi_responses_example(api_error_case: ApiErrorCase, responses: dict):
    (
        responses
            .setdefault(str(api_error_case.status_code), {})
            .setdefault("content", {})
            .setdefault("application/json", {})
            .setdefault("examples", {})
            .setdefault(api_error_case.error_code, {
                "summary": api_error_case.error_code,
                "value": api_error_case_to_back_api_error(api_error_case).model_dump(),
            })
    )
