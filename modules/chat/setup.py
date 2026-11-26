from fastapi import FastAPI

from modules.chat.postgres.tables.chat import PgChat
from modules.chat.postgres.tables.chat_to_user import PgChatToUser


def setup_chat(app: FastAPI):
    chat_table = PgChat
    chat_to_user_table = PgChatToUser