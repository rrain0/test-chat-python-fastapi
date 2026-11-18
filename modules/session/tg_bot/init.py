from fastapi import FastAPI

from modules.session.tg_bot.postgres.tg_bot_session import PgTgBotSession


def init_tg_bot_session(app: FastAPI):
    tg_bot_session_table = PgTgBotSession
