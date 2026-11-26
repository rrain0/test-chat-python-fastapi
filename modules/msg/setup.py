from fastapi import FastAPI

from modules.msg.postgres.tables.msg import DbMsg
from modules.msg.endpoints.msg_post import router_msg_post


def setup_msg(app: FastAPI):
    msg_table = DbMsg
    app.include_router(router_msg_post)
