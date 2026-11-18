from fastapi import FastAPI

from modules.chat.db_tables.chat import DbChat
from modules.chat.db_tables.chat_to_user import DbChatToUser


def init_chat(app: FastAPI):
    chat_table = DbChat
    chat_to_user_table = DbChatToUser