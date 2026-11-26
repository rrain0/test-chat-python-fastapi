from modules.session.web.postgres.table.web_session import PgWebSession
from modules.session.web.redis.entity.web_session import RdWebSession


def pg_to_rd_web_session(pg_session: PgWebSession) -> RdWebSession:
    return RdWebSession(
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
