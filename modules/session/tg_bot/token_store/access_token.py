from fastapi import Request


def get_tg_bot_access_token(request: Request):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return None
    if not auth_header.startswith("Bearer "):
        return None

    access_token_str = auth_header[len("Bearer "):]

    if not access_token_str:
        return None
    if not access_token_str.startswith("tg_bot_"):
        return None

    return access_token_str
