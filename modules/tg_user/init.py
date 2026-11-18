from fastapi import FastAPI

from modules.tg_user.db_tables.tg_user import PgTgUser
from modules.tg_user.endpoints.login_post import router_tg_user_login
from modules.tg_user.endpoints.msg_post import router_tg_user_msg
from modules.tg_user.endpoints.signup_post import router_tg_user_signup


def init_tg_user(app: FastAPI):
    tg_user_table = PgTgUser
    app.include_router(router_tg_user_login)
    app.include_router(router_tg_user_signup)
    app.include_router(router_tg_user_msg)