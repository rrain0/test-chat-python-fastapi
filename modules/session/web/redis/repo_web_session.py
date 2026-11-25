from uuid import UUID


def rd_get_user_web_session_key(user_id: UUID, session_id: UUID):
    return (
        f"session:web"
        f":user_id:{str(user_id)}"
        f":session_id:{str(session_id)}"
    )
