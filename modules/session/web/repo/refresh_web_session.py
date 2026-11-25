import asyncio
from uuid import uuid7

from redis_fastapi import AsyncRedisDep

from core.postgres.init import AsyncPostgresDep
from modules.session.unauthorized_error import unauthorized_exception
from modules.session.web.convert.pg_web_session_to_rd_web_session import pg_web_session_to_rd_web_session
from modules.session.web.jwt_access.create_web_access_token import create_web_access_token
from modules.session.web.jwt_refresh.create_web_refresh_token import create_web_refresh_token
from modules.session.web.jwt_refresh.decode_web_refresh_token import decode_web_refresh_token
from modules.session.web.postgres.get_web_session_by_id_by_user_id import pg_get_web_session_by_id_by_user_id
from modules.session.web.postgres.upsert_web_session_by_id import pg_upsert_web_session_by_id
from modules.session.web.postgres.web_session import PgWebSession, PgWebSessionUpdate
from modules.session.web.redis.repo_grace_web_session import rd_get_grace_web_session
from modules.session.web.redis.repo_prev_web_session import rd_get_prev_web_session, rd_set_prev_web_session
from modules.session.web.redis.repo_current_web_session import rd_get_current_web_session, rd_set_current_web_session
from modules.session.web.redis.repo_web_session import rd_get_user_web_session_key
from modules.session.web.repo.remove_web_session import remove_web_session
from shared.utils.datetimes.now import now
from shared.utils.rediss.redis_watchdog_lock import redis_watchdog_lock


async def commit_refresh_web_session(
        refresh_token_str: str,
        user_ip: str | None,
        user_agent_str: str | None,
        postgres: AsyncPostgresDep,
        redis: AsyncRedisDep,
):
    try:
        refresh_token = decode_web_refresh_token(refresh_token_str)
    except Exception as ex:
        raise unauthorized_exception() from ex

    async with redis_watchdog_lock(
        redis,
        rd_get_user_web_session_key(refresh_token.user_id, refresh_token.session_id),
    ):
        await asyncio.sleep(8)

        rd_web_session = await rd_get_current_web_session(
            user_id=refresh_token.user_id,
            session_id=refresh_token.session_id,
            redis=redis,
        )
        rd_prev_web_session = await rd_get_prev_web_session(
            user_id=refresh_token.user_id,
            session_id=refresh_token.session_id,
            redis=redis,
        )
        rd_grace_web_session = await rd_get_grace_web_session(
            user_id=refresh_token.user_id,
            session_id=refresh_token.session_id,
            redis=redis,
        )

        # Cache the session from db
        if not rd_web_session:
            pg_web_session = await pg_get_web_session_by_id_by_user_id(
                id=refresh_token.session_id,
                user_id=refresh_token.user_id,
                postgres=postgres,
            )
            if pg_web_session: rd_web_session = pg_web_session_to_rd_web_session(pg_web_session)

        # Check if session exists
        if not rd_web_session:
            raise unauthorized_exception()

        last_active_at = now()

        # TODO add repeated task to check and remove expired postgres sessions

        # Check if session expired
        if rd_web_session.refresh_token_expires_at < last_active_at:
            # Remove expired session
            await remove_web_session(
                user_id=refresh_token.user_id,
                session_id=refresh_token.session_id,
                postgres=postgres,
                redis=redis,
            )
            await postgres.commit()
            raise unauthorized_exception()

        rt_id = refresh_token.id
        curr_rt_id = rd_web_session.refresh_token_id
        prev_rt_id = rd_prev_web_session.refresh_token_id if rd_prev_web_session else None
        grace_rt_id = rd_grace_web_session.refresh_token_id if rd_grace_web_session else None

        # Check if refresh token is active
        if rt_id not in (curr_rt_id, prev_rt_id, grace_rt_id):
            # Suspicious activity detected - performing session removal
            await remove_web_session(
                user_id=refresh_token.user_id,
                session_id=refresh_token.session_id,
                postgres=postgres,
                redis=redis,
            )
            await postgres.commit()
            raise unauthorized_exception()

        # Check token expiration
        if refresh_token.expires_at < last_active_at:
            raise unauthorized_exception()


        # CASE 1
        # Check if using current refresh token and can generate new one
        if rt_id == curr_rt_id and not rd_prev_web_session and not rd_grace_web_session:
            # Create new refresh token
            new_refresh_token_id = uuid7()
            new_refresh_token_str, new_refresh_token = create_web_refresh_token(
                id=new_refresh_token_id,
                session_id=refresh_token.session_id,
                created_at=last_active_at,
                user_id=refresh_token.user_id,
                user_username=refresh_token.user_username,
            )

            pg_web_session = PgWebSession(
                id=new_refresh_token.session_id,
                created_at=rd_web_session.created_at,
                updated_at=last_active_at,
                refresh_token_id=new_refresh_token.id,
                refresh_token_created_at=new_refresh_token.created_at,
                refresh_token_expires_at=new_refresh_token.expires_at,
                user_id=new_refresh_token.user_id,
                last_active_at=last_active_at,
                last_active_at_ip=user_ip,
                last_active_at_device=user_agent_str,
            )

            # Create new access token
            new_access_token_id = uuid7()
            new_access_token_str, new_access_token = create_web_access_token(
                id=new_access_token_id,
                session_id=new_refresh_token.session_id,
                refresh_token_id=new_refresh_token.id,
                created_at=last_active_at,
                user_id=new_refresh_token.user_id,
                user_username=new_refresh_token.user_username,
            )

            await pg_upsert_web_session_by_id(
                pg_web_session=pg_web_session,
                pg_web_session_update=PgWebSessionUpdate(
                    updated_at=pg_web_session.updated_at,
                    refresh_token_id=pg_web_session.refresh_token_id,
                    refresh_token_created_at=pg_web_session.refresh_token_created_at,
                    refresh_token_expires_at=pg_web_session.refresh_token_expires_at,
                    last_active_at=pg_web_session.last_active_at,
                    last_active_at_ip=pg_web_session.last_active_at_ip,
                    last_active_at_device=pg_web_session.last_active_at_device,
                ),
                postgres=postgres,
            )
            await postgres.commit()

            # Move web session to prev
            rd_prev_web_session = rd_web_session
            rd_new_web_session = pg_web_session_to_rd_web_session(pg_web_session)

            await rd_set_prev_web_session(rd_prev_web_session, redis)
            await rd_set_current_web_session(rd_new_web_session, redis)

            return new_access_token_str, new_access_token, new_refresh_token_str, new_refresh_token



        # CASE 2
        # Check if using current refresh token and has prev or grace sessions.
        # If has prev or grace session then do not generate new refresh token, generate only new access token
        if rt_id == curr_rt_id and rd_prev_web_session or rd_grace_web_session:
            # Create new access token
            new_access_token_id = uuid7()
            new_access_token_str, new_access_token = create_web_access_token(
                id=new_access_token_id,
                session_id=refresh_token.session_id,
                refresh_token_id=refresh_token.id,
                created_at=last_active_at,
                user_id=refresh_token.user_id,
                user_username=refresh_token.user_username,
            )

            # Update current session (not prev and not grace session) and save only to redis
            rd_web_session.last_active_at = last_active_at
            rd_web_session.last_active_at_ip = user_ip
            rd_web_session.last_active_at_device = user_agent_str
            await rd_set_current_web_session(
                web_session=rd_web_session,
                redis=redis,
            )

            return new_access_token_str, new_access_token, refresh_token_str, refresh_token



        # CASE 3
        # Check if using prev or grace refresh token
        if rt_id in (prev_rt_id, grace_rt_id):
            # Recreate the same new refresh token
            new_refresh_token_str, new_refresh_token = create_web_refresh_token(
                id=rd_web_session.refresh_token_id,
                session_id=rd_web_session.id,
                created_at=rd_web_session.refresh_token_created_at,
                user_id=refresh_token.user_id,
                user_username=refresh_token.user_username,
            )

            # Create new access token
            new_access_token_id = uuid7()
            new_access_token_str, new_access_token = create_web_access_token(
                id=new_access_token_id,
                session_id=new_refresh_token.session_id,
                refresh_token_id=new_refresh_token.id,
                created_at=last_active_at,
                user_id=new_refresh_token.user_id,
                user_username=new_refresh_token.user_username,
            )

            # Update current session (not prev and not grace session) and save only to redis
            rd_web_session.last_active_at = last_active_at
            rd_web_session.last_active_at_ip = user_ip
            rd_web_session.last_active_at_device = user_agent_str
            await rd_set_current_web_session(
                web_session=rd_web_session,
                redis=redis,
            )

            return new_access_token_str, new_access_token, new_refresh_token_str, new_refresh_token



    # Runtime unreachable
    raise unauthorized_exception()
