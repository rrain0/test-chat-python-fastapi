import os
from datetime import timedelta

from shared.utils.datetimes.duration import duration


POSTGRES_URL: str = os.getenv("POSTGRES_URL")

REDIS_URL: str = os.getenv("REDIS_URL")

WEB_ACCESS_TOKEN_SECRET: str = os.getenv("WEB_ACCESS_TOKEN_SECRET")
WEB_ACCESS_TOKEN_LIFETIME: timedelta = duration(os.getenv("WEB_ACCESS_TOKEN_LIFETIME"))

WEB_REFRESH_TOKEN_SECRET: str = os.getenv("WEB_REFRESH_TOKEN_SECRET")
WEB_REFRESH_TOKEN_LIFETIME: timedelta = duration(os.getenv("WEB_REFRESH_TOKEN_LIFETIME"))
WEB_REFRESH_TOKEN_GRACE_PERIOD: timedelta = duration(os.getenv("WEB_REFRESH_TOKEN_GRACE_PERIOD"))

TG_BOT_ACCESS_TOKEN_SECRET: str = os.getenv("TG_BOT_ACCESS_TOKEN_SECRET")
TG_BOT_ACCESS_TOKEN_LIFETIME: timedelta = duration(os.getenv("TG_BOT_ACCESS_TOKEN_LIFETIME"))
