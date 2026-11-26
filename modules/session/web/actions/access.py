from modules.auth.api_errors.unauthorized_utils import unauthorized_exception
from modules.session.web.mappers.pg_to_rd_web_session import pg_to_rd_web_session
from modules.session.web.jwt_access.decode import decode_web_access_token
from modules.session.web.postgres.repo.get_by_id_by_user_id import pg_get_web_session_by_id_by_user_id
from modules.session.web.redis.repo.grace import rd_get_grace_web_session, rd_set_grace_web_session
from modules.session.web.redis.repo.prev import rd_get_prev_web_session, rd_delete_prev_web_session
from modules.session.web.redis.repo.current import rd_set_current_web_session, rd_get_current_web_session
from modules.session.web.redis.key.keys import rd_get_user_web_session_key
from modules.session.web.actions.remove import remove_web_session
from shared.utils.datetimes.now import now
from shared.utils.postgres.async_postgres import AsyncPostgres
from shared.utils.rediss.async_redis import AsyncRedis
from shared.utils.rediss.watchdog_lock import redis_watchdog_lock


async def commit_access_web_session(
        access_token_str: str,
        user_ip: str | None,
        user_agent_str: str | None,
        postgres: AsyncPostgres,
        redis: AsyncRedis,
):
    try: access_token = decode_web_access_token(access_token_str)
    except Exception as ex:
        raise unauthorized_exception() from ex

    async with redis_watchdog_lock(
        rd_get_user_web_session_key(access_token.user_id, access_token.session_id),
        redis,
    ):
        rd_web_session = await rd_get_current_web_session(
            user_id=access_token.user_id,
            session_id=access_token.session_id,
            redis=redis,
        )
        rd_prev_web_session = await rd_get_prev_web_session(
            user_id=access_token.user_id,
            session_id=access_token.session_id,
            redis=redis,
        )
        rd_grace_web_session = await rd_get_grace_web_session(
            user_id=access_token.user_id,
            session_id=access_token.session_id,
            redis=redis,
        )

        # Cache the session from db
        if not rd_web_session:
            pg_web_session = await pg_get_web_session_by_id_by_user_id(
                id=access_token.session_id,
                user_id=access_token.user_id,
                postgres=postgres,
            )
            if pg_web_session: rd_web_session = pg_to_rd_web_session(pg_web_session)

        # Check if session exists
        if not rd_web_session:
            raise unauthorized_exception()

        last_active_at = now()

        # TODO add repeated task to check and remove expired postgres sessions

        # Check if session expired
        if rd_web_session.refresh_token_expires_at < last_active_at:
            # Remove expired session
            await remove_web_session(
                user_id=access_token.user_id,
                session_id=access_token.session_id,
                postgres=postgres,
                redis=redis,
            )
            await postgres.commit()
            raise unauthorized_exception()

        access_rt_id = access_token.refresh_token_id
        curr_rt_id = rd_web_session.refresh_token_id
        prev_rt_id = rd_prev_web_session.refresh_token_id if rd_prev_web_session else None
        grace_rt_id = rd_grace_web_session.refresh_token_id if rd_grace_web_session else None

        # Check if refresh token is active
        if access_rt_id not in (curr_rt_id, prev_rt_id, grace_rt_id):
            # Suspicious activity detected - performing session removal
            await remove_web_session(
                user_id=access_token.user_id,
                session_id=access_token.session_id,
                postgres=postgres,
                redis=redis,
            )
            await postgres.commit()
            raise unauthorized_exception()

        # Check token expiration
        if access_token.expires_at < last_active_at:
            raise unauthorized_exception()



        # Check if using current refresh token
        if access_rt_id == curr_rt_id:
            # Update current session and save only to redis
            rd_web_session.last_active_at = last_active_at
            rd_web_session.last_active_at_ip = user_ip
            rd_web_session.last_active_at_device = user_agent_str

            await rd_set_current_web_session(
                web_session=rd_web_session,
                redis=redis,
            )

            # Move prev web session to grace
            if rd_prev_web_session:
                await rd_set_grace_web_session(
                    rd_prev_web_session,
                    grace_start_at=last_active_at,
                    redis=redis,
                )
                await rd_delete_prev_web_session(
                    user_id=access_token.user_id,
                    session_id=access_token.session_id,
                    redis=redis,
                )

            return access_token



        # Check if using prev or grace refresh token
        if access_rt_id in (prev_rt_id, grace_rt_id):
            # Update current session (not prev and not grace session) and save only to redis
            rd_web_session.last_active_at = last_active_at
            rd_web_session.last_active_at_ip = user_ip
            rd_web_session.last_active_at_device = user_agent_str

            await rd_set_current_web_session(
                web_session=rd_web_session,
                redis=redis,
            )

            return access_token



    # Runtime unreachable
    raise unauthorized_exception()
