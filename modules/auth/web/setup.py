from fastapi import FastAPI

from modules.auth.web.endpoints.refresh_post import router_auth_web_refresh



def setup_auth_web(app: FastAPI):
    app.include_router(router_auth_web_refresh)
