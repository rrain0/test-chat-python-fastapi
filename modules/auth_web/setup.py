from fastapi import FastAPI

from modules.auth_web.endpoints.logout_post import router_auth_web_logout_post
from modules.auth_web.endpoints.login_post import router_auth_web_login_post



def setup_auth_web(app: FastAPI):
    app.include_router(router_auth_web_login_post)
    app.include_router(router_auth_web_logout_post)
