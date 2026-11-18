from typing import Any, Dict

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from shared.backend.modules.error.api_model.error import BackApiError


class ApiErrorCase(BaseModel):
    status_code: int
    error_code: str
    error_msg: str = ""
    error_detail: Any | None = None

    def to_back_api_error(self):
        return BackApiError(
            error_code=self.error_code,
            error_msg=self.error_msg,
            error_detail=self.error_detail,
        )

    def to_exception(self):
        return ApiErrorCaseException(self)

    def to_json_response(self):
        return JSONResponse(
            status_code=self.status_code,
            content=jsonable_encoder(self.to_back_api_error())
        )

    def add_example_to_openapi_responses(self, responses: Dict) -> 'ApiErrorCase':
        (
            responses
                .setdefault(str(self.status_code), {})
                .setdefault('content', {})
                .setdefault('application/json', {})
                .setdefault('examples', {})
                .setdefault(self.error_code, {
                    'summary': self.error_code,
                    'value': self.to_back_api_error().model_dump(),
                })
        )
        return self



class ApiErrorCaseException(Exception):
    def __init__(self, api_error_case: ApiErrorCase):
        self.api_error_case = api_error_case



