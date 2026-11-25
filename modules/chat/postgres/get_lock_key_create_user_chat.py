from uuid import UUID


def pg_get_lock_key_create_user_chat(user_id: UUID):
    return f"create_user_chat:{user_id}"
