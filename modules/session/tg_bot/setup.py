from fastapi import FastAPI

from modules.session.tg_bot.postgres.tables.tg_bot_session import PgTgBotSession


def setup_tg_bot_session(app: FastAPI):
    tg_bot_session_table = PgTgBotSession
