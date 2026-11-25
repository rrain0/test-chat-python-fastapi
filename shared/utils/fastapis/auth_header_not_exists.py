from fastapi import Request


def auth_header_not_exists(request: Request) -> bool:
    return request.headers.get("Authorization") is None
