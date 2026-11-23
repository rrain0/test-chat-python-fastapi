import jwt

from core.config.env import TG_BOT_ACCESS_TOKEN_SECRET
from shared.backend.modules.session.tg_bot.jwt_access.tg_bot_access_token import TgBotAccessToken


def decode_tg_bot_access_token(token_str: str) -> TgBotAccessToken:
    payload = jwt.decode(
        jwt=token_str[len("tg_bot_"):],
        key=TG_BOT_ACCESS_TOKEN_SECRET,
        algorithms=["HS256"],
        options={
            "verify_signature": True,    # Ensure the signature is valid
            "verify_exp": False,         # Turn off the expiration check
            "require": ["exp"],          # Raise an error if the token has no "exp" claim at all
        }
    )

    try: token = TgBotAccessToken.model_validate(payload)
    except:
        raise jwt.InvalidTokenError

    if token.type != "TgBotAccessToken":
        raise jwt.InvalidTokenError

    return token