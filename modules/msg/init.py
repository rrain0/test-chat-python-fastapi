from fastapi import FastAPI

from modules.msg.db_tables.msg import DbMsg


def init_msg(app: FastAPI):
    msg_table = DbMsg
