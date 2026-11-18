from fastapi import Request


def get_client_ip(request: Request) -> str | None:
    # 1. Check X-Forwarded-For (can be a comma-separated list if multiple proxies exist)
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        # The first IP in the list is the original client
        return x_forwarded_for.split(',')[0].strip()

    # 2. Fallback to X-Real-IP if provided
    x_real_ip = request.headers.get('X-Real-IP')
    if x_real_ip:
        return x_real_ip

    # 3. Fallback to the direct connection socket
    client = request.client
    if client:
        return client.host

    return None
