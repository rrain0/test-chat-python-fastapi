from fastapi import FastAPI

from modules.auth_tg_bot.endpoints.logout_post import router_auth_tg_bot_logout_post
from modules.auth_tg_bot.endpoints.login_post import router_auth_tg_bot_login_post



def setup_auth_tg_bot(app: FastAPI):
    app.include_router(router_auth_tg_bot_login_post)
    app.include_router(router_auth_tg_bot_logout_post)
