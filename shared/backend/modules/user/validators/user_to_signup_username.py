import re


def validate_user_to_signup_username(username: str):
    # Проверяем длину юзернейма (от 3 до 32 символов)
    if not (4 <= len(username) <= 32):
        raise ValueError("Username length must be in range 4..32")

    if not bool(re.fullmatch(r"^[a-z][a-z0-9_]*$", username)):
        raise ValueError("Username must be of pattern '^[a-z][a-z0-9_]*$'")
