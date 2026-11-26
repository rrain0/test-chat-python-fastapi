import jwt

from core.config.env import WEB_REFRESH_TOKEN_SECRET
from modules.session_web.jwt_refresh.token import WebRefreshToken


def decode_web_refresh_token(token: str):
    payload = jwt.decode(
        jwt=token[len("web_"):],
        key=WEB_REFRESH_TOKEN_SECRET,
        algorithms=["HS256"],
        options={
            "verify_signature": True,    # Ensure the signature is valid
            "verify_exp": False,         # Turn off the expiration check
            "require": ["exp"],          # Raise an error if the token has no "exp" claim at all
        }
    )

    try: token = WebRefreshToken.model_validate(payload)
    except:
        raise jwt.InvalidTokenError

    if token.type != "WebRefreshToken":
        raise jwt.InvalidTokenError

    return token
