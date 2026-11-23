from fastapi import FastAPI

from modules.msg.postgres.msg import DbMsg
from modules.msg.endpoints.msg_post import router_msg


def init_msg(app: FastAPI):
    msg_table = DbMsg
    app.include_router(router_msg)
