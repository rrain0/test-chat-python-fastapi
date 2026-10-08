import bcrypt


# Функция для создания безопасного хэша пароля
def hash_password(password: str) -> str:
    # Случайная соль для каждого пароля
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(pwd: str, pwd_hash: str) -> bool:
    return bcrypt.checkpw(pwd.encode('utf-8'), pwd_hash.encode('utf-8'))

