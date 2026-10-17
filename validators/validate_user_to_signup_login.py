def validate_user_to_signup_login(login: str):
    # Проверяем длину логина (от 1 до 30 символов)
    if not (1 <= len(login) <= 30):
        raise ValueError("Login length must be in range 1..30")
