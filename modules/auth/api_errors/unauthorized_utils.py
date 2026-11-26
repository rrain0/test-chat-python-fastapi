from core.api_error.utils import api_error_case_to_exception
from shared.backend.modules.auth.api_errors.unauthorized import unauthorized_error_case


def unauthorized_exception():
    return api_error_case_to_exception(unauthorized_error_case)
