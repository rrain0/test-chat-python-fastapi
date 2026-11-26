from fastapi import FastAPI

from modules.session_web.postgres.tables.web_session import PgWebSession
from modules.session_web.endpoints.refresh_post import router_auth_web_refresh



def setup_web_session(app: FastAPI):
    web_session_table = PgWebSession
    app.include_router(router_auth_web_refresh)
