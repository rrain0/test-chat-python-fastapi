import os
from datetime import timedelta

from shared.utils.datetimes.duration_to_timedelta import duration_to_timedelta


POSTGRES_URL: str = os.getenv('POSTGRES_URL')

REDIS_URL: str = os.getenv('REDIS_URL')
REDIS_PREFIX: str = os.getenv('REDIS_PREFIX')

WEB_ACCESS_TOKEN_SECRET: str = os.getenv('WEB_ACCESS_TOKEN_SECRET')
WEB_ACCESS_TOKEN_LIFETIME: timedelta = duration_to_timedelta(os.getenv('WEB_ACCESS_TOKEN_LIFETIME'))

WEB_REFRESH_TOKEN_SECRET: str = os.getenv('WEB_REFRESH_TOKEN_SECRET')
WEB_REFRESH_TOKEN_LIFETIME: timedelta = duration_to_timedelta(os.getenv('WEB_REFRESH_TOKEN_LIFETIME'))
WEB_REFRESH_TOKEN_GRACE_PERIOD: timedelta = duration_to_timedelta(os.getenv('WEB_REFRESH_TOKEN_GRACE_PERIOD'))

TG_BOT_ACCESS_TOKEN_SECRET: str = os.getenv('TG_BOT_ACCESS_TOKEN_SECRET')
TG_BOT_ACCESS_TOKEN_LIFETIME: timedelta = duration_to_timedelta(os.getenv('TG_BOT_ACCESS_TOKEN_LIFETIME'))

TG_BOT_SESSION_TOKEN_SECRET: str = os.getenv('TG_BOT_SESSION_TOKEN_SECRET')
TG_BOT_SESSION_TOKEN_LIFETIME: timedelta = duration_to_timedelta(os.getenv('TG_BOT_SESSION_TOKEN_LIFETIME'))
