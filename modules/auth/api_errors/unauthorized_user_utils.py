from core.api_error.utils import api_error_case_to_exception
from shared.backend.modules.auth.api_errors.unauthorized_user import unauthorized_user_error_case


def unauthorized_user_exception():
    return api_error_case_to_exception(unauthorized_user_error_case)
