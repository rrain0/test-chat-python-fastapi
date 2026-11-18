from modules.session.web.postgres.web_session import PgWebSession
from modules.session.web.redis.web_session import RdWebSessionByToken


def pg_web_session_to_rd_web_session(pg_session: PgWebSession) -> RdWebSessionByToken:
    return RdWebSessionByToken(
        id=pg_session.id,
        created_at=pg_session.created_at,
        refresh_token_id=pg_session.refresh_token_id,
        refresh_token_created_at=pg_session.refresh_token_created_at,
        refresh_token_expires_at=pg_session.refresh_token_expires_at,
        user_id=pg_session.user_id,
        last_active_at=pg_session.last_active_at,
        last_active_at_ip=pg_session.last_active_at_ip,
        last_active_at_device=pg_session.last_active_at_device,
    )
