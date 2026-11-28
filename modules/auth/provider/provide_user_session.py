import traceback
from typing import Annotated
from fastapi import Depends
from fastapi import Request
from redis_fastapi import AsyncRedisDep

from core.postgres.setup import AsyncPostgresDep
from modules.auth.api_errors.unauthorized_user_utils import unauthorized_user_exception
from modules.auth.model.app_session import AppSession
from modules.session_tg_bot.jwt_access.decode import decode_tg_bot_access_token
from modules.session_tg_bot.token_store.access_token import get_tg_bot_access_token
from modules.session_web.actions.access import commit_access_web_session
from modules.session_web.token_store.access_token import get_web_access_token
from shared.utils.fastapis.get_client_ip import get_client_ip
from shared.utils.fastapis.get_client_user_agent_str import get_client_user_agent_str



async def provide_user_session(
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



    tg_bot_access_token_str = get_tg_bot_access_token(request)
    if tg_bot_access_token_str:
        # TODO provide tg_bot session
        try:
            tg_bot_token = decode_tg_bot_access_token(tg_bot_access_token_str)

            print("TG_BOT_TOKEN", tg_bot_token)

            # TODO check expiration
            # TODO check redis & postgres here
            # app_session = AppSession(
            #     session_id=tg_bot_token.session_id,
            #     user_id=tg_bot_token.user_id,
            #     user_username=tg_bot_token.user_username,
            #     tg_bot_access_token=tg_bot_token,
            # )
            # return app_session
        except Exception as ex:
            traceback.print_exc()
            raise unauthorized_user_exception() from ex

    raise unauthorized_user_exception()



ProvideAppSessionDep = Annotated[AppSession, Depends(provide_user_session)]
