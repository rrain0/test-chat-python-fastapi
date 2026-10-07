import re
from pydantic import BaseModel
from model_api.ApiError import ApiError


class UserCreate(BaseModel):
    login: str
    pwd: str

    def validate_after(self) -> ApiError | None:
        # Проверяем длину логина (от 1 до 30 символов)
        if not (1 <= len(self.login) <= 30):
            return ApiError(
                error_code="LOGIN_LEN_INVALID",
                description="Длина логина должна быть от 1 до 30 символов"
            )

        # Проверяем длину пароля (от 8 до 100 символов)
        if not (8 <= len(self.pwd) <= 100):
            return ApiError(
                error_code="PWD_LEN_INVALID",
                description="Длина пароля должна быть от 8 до 100 символов"
            )

        # Проверяем сложность пароля (хотя бы одна буква и одна цифра)
        has_digit = re.search(r"\d", self.pwd)
        has_nondigit = re.search(r"\D", self.pwd)

        if not (has_nondigit and has_digit):
            return ApiError(
                error_code="PWD_COMPLEXITY_TOO_LOW",
                description="Пароль должен содержать цифры и не цифры"
            )

        return None