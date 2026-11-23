from uuid import UUID

from core.config.env import REDIS_PREFIX


def rd_get_user_web_session_key(user_id: UUID, session_id: UUID):
    return (
        f"{REDIS_PREFIX}:session:web"
        f":user_id:{str(user_id)}"
        f":session_id:{str(session_id)}"
    )
