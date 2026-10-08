import re
from pydantic import BaseModel, model_validator


class ApiUserCreate(BaseModel):
    login: str
    pwd: str

    @model_validator(mode="after")
    def validate_after(self) -> "ApiUserCreate":
        # Проверяем длину логина (от 1 до 30 символов)
        if not (1 <= len(self.login) <= 30):
            raise ValueError("Login length must be in range 1..30")

        # Проверяем длину пароля (от 8 до 100 символов)
        if not (8 <= len(self.pwd) <= 100):
            raise ValueError("Password length must be in range 8..100")

        # Проверяем сложность пароля (хотя бы одна буква и одна цифра)
        has_digit = re.search(r"\d", self.pwd)
        has_nondigit = re.search(r"\D", self.pwd)
        if not (has_nondigit and has_digit):
            raise ValueError("Password must contain digits and non-digits")

        return self