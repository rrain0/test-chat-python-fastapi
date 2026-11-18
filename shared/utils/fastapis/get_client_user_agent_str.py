from fastapi import Request


def get_client_user_agent_str(request: Request) -> str | None:
    user_agent_str = request.headers.get('User-Agent')
    return user_agent_str