from fastapi import FastAPI

from modules.chat.postgres.chat import DbChat
from modules.chat.postgres.chat_to_user import DbChatToUser


def init_chat(app: FastAPI):
    chat_table = DbChat
    chat_to_user_table = DbChatToUser