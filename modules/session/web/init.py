from fastapi import FastAPI

from modules.session.web.postgres.web_session import PgWebSession


def init_web_session(app: FastAPI):
    web_session_table = PgWebSession
