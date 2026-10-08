import re



def validate_user_signup_login(login: str):
    # Проверяем длину логина (от 1 до 30 символов)
    if not (1 <= len(login) <= 30):
        raise ValueError("Login length must be in range 1..30")



def validate_user_signup_password(pwd: str):
    # Проверяем длину пароля (от 8 до 100 символов)
    if not (8 <= len(pwd) <= 100):
        raise ValueError("Password length must be in range 8..100")

    # Проверяем сложность пароля (хотя бы одна буква и одна цифра)
    has_digit = re.search(r"\d", pwd)
    has_nondigit = re.search(r"\D", pwd)
    if not (has_nondigit and has_digit):
        raise ValueError("Password must contain digits and non-digits")
