from datetime import datetime

from fastapi import Response, Request


def get_web_refresh_token(
        request: Request,
):
    refresh_token_str = request.cookies.get("WebRefreshToken", "")
    if not refresh_token_str:
        return None
    if not refresh_token_str.startswith("web_"):
        return None
    return refresh_token_str


def add_web_refresh_token(
        response: Response,
        refresh_token_str: str,
        expires_at: datetime,
):
    response.set_cookie(
        key="WebRefreshToken",
        value=refresh_token_str,
        httponly=True,
        #max_age=cookie_max_age,
        expires=expires_at,
        # Send cookie with request only when request to the same site (2 main domain parts are the same).
        # With exception allowing to send cookies via <a href="..."> under different site.
        samesite="lax",
        secure=True, # Set to False ONLY for local non-HTTPS development
        path="/api/auth/web/refresh", # Limits cookie transmission strictly to this path & subpaths
    )



def delete_web_refresh_token(
        response: Response,
):
    response.delete_cookie(
        key="WebRefreshToken",
        httponly=True,
        samesite="lax",
        secure=True, # Set to False ONLY for local non-HTTPS development
        path="/api/auth/web/refresh", # Limits cookie transmission strictly to auth endpoints
    )
