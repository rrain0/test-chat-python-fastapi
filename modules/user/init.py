from fastapi import FastAPI

from modules.user.postgres.user import PgUser
from modules.user.endpoints.logout_post import router_user_logout
from modules.user.endpoints.signup_post import router_user_signup
from modules.user.endpoints.login_post import router_user_login
from modules.user.endpoints.current_get import router_user_current



def init_user(app: FastAPI):
    user_table = PgUser
    app.include_router(router_user_signup)
    app.include_router(router_user_login)
    app.include_router(router_user_current)
    app.include_router(router_user_logout)
