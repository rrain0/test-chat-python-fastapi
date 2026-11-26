from uuid import UUID


def pg_get_create_user_chat_key(user_id: UUID):
    return f"create_user_chat:{user_id}"
