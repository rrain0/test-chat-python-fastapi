import jwt

from core.config.env import WEB_ACCESS_TOKEN_SECRET
from modules.session.web.jwt_access.token import WebAccessToken


def decode_web_access_token(token_str: str) -> WebAccessToken:
    payload = jwt.decode(
        jwt=token_str[len("web_"):],
        key=WEB_ACCESS_TOKEN_SECRET,
        algorithms=["HS256"],
        options={
            "verify_signature": True,    # Ensure the signature is valid
            "verify_exp": False,         # Turn off the expiration check
            "require": ["exp"],          # Raise an error if the token has no "exp" claim at all
        }
    )

    try: token = WebAccessToken.model_validate(payload)
    except:
        raise jwt.InvalidTokenError

    if token.type != "WebAccessToken":
        raise jwt.InvalidTokenError

    return token
