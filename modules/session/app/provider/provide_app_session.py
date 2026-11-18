from typing import Annotated
from fastapi import Depends
from redis_fastapi import AsyncRedisDep
from fastapi import Request

from core.postgres.init import AsyncPostgresDep
from modules.session.app.model.app_session import AppSession
from modules.session.tg_bot.jwt_access.decode_tg_bot_access_token import decode_tg_bot_access_token
from modules.session.unauthorized_error import unauthorized_exception
from modules.session.web.repo.access_web_session import commit_access_web_session
from modules.session.web.token_store.access_token import get_web_access_token
from shared.utils.fastapis.get_client_ip import get_client_ip
from shared.utils.fastapis.get_client_user_agent_str import get_client_user_agent_str


async def provide_app_session(
        request: Request,
        postgres: AsyncPostgresDep,
        redis: AsyncRedisDep,
) -> AppSession:
    web_access_token_str = get_web_access_token(request)
    if web_access_token_str:
        access_token = await commit_access_web_session(
            access_token_str = web_access_token_str,
            user_ip = get_client_ip(request),
            user_agent_str = get_client_user_agent_str(request),
            postgres = postgres,
            redis = redis,
        )

        app_session = AppSession(
            session_id=access_token.session_id,
            user_id=access_token.user_id,
            user_username=access_token.user_username,
            web_access_token=access_token,
        )
        return app_session



    # TODO provide tg_bot session
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        raise unauthorized_exception()
    try:
        if web_access_token_str.startswith('tg_bot_'):
            tg_bot_token = decode_tg_bot_access_token(web_access_token_str)
            # TODO check expiration
            # TODO check redis & postgres here
            app_session = AppSession(
                session_id=tg_bot_token.session_id,
                user_id=tg_bot_token.user_id,
                user_username=tg_bot_token.user_username,
                tg_bot_access_token=tg_bot_token,
            )
            return app_session
    except Exception as ex:
        raise unauthorized_exception() from ex

    raise unauthorized_exception()



ProvideAppSessionDep = Annotated[AppSession, Depends(provide_app_session)]
