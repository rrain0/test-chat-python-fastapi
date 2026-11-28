from shared.backend.core.api_error.api_error_case import ApiErrorCase


class ApiErrorCaseException(Exception):
    def __init__(self, api_error_case: ApiErrorCase):
        self.api_error_case = api_error_case
        super().__init__(
            f"[{api_error_case.status_code}] "
            f"{api_error_case.error_code}: "
            f"{api_error_case.error_msg}"
        )
