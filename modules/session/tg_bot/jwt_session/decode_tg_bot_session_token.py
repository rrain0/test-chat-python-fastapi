import jwt

from core.config.env import TG_BOT_SESSION_TOKEN_SECRET
from modules.session.tg_bot.jwt_session.tg_bot_session_token import TgBotSessionToken


def decode_tg_bot_session_token(token: str):
    payload = jwt.decode(
        jwt=token,
        key=TG_BOT_SESSION_TOKEN_SECRET,
        algorithms=['HS256'],
        options={
            'verify_signature': True,    # Ensure the signature is valid
            'verify_exp': False,         # Turn off the expiration check
            'require': ['exp'],          # Raise an error if the token has no 'exp' claim at all
        }
    )

    try: token = TgBotSessionToken.model_validate(payload)
    except:
        raise jwt.InvalidTokenError

    if token.type != 'TgBotSessionToken':
        raise jwt.InvalidTokenError

    return token
