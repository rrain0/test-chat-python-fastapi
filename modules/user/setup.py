from fastapi import FastAPI

from modules.user.postgres.tables.user import PgUser
from modules.user.endpoints.signup_post import router_user_signup_post
from modules.user.endpoints.current_get import router_user_current_get



def setup_user(app: FastAPI):
    user_table = PgUser
    app.include_router(router_user_signup_post)
    app.include_router(router_user_current_get)
