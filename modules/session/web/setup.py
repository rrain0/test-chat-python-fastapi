from fastapi import FastAPI

from modules.session.web.postgres.table.web_session import PgWebSession


def setup_web_session(app: FastAPI):
    web_session_table = PgWebSession
