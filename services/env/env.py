import os
from datetime import timedelta

from utils.datetimes import parse_duration

# Format: postgresql://<user>:<password>@<host>:<port>/<database_name>
POSTGRES_URL: str = os.getenv("POSTGRES_URL")

# Format: redis://<user>:<password>@<host>:<port>/<database_index>
REDIS_URL: str = os.getenv("REDIS_URL")
REDIS_PREFIX: str = os.getenv("REDIS_PREFIX")

USER_ACCESS_TOKEN_SECRET: str = os.getenv("USER_ACCESS_TOKEN_SECRET")
USER_ACCESS_TOKEN_LIFETIME: timedelta = timedelta(
    milliseconds=parse_duration(os.getenv("USER_ACCESS_TOKEN_LIFETIME"))
)

TG_USER_ACCESS_TOKEN_SECRET: str = os.getenv("TG_USER_ACCESS_TOKEN_SECRET")
TG_USER_ACCESS_TOKEN_LIFETIME: timedelta = timedelta(
    milliseconds=parse_duration(os.getenv("TG_USER_ACCESS_TOKEN_LIFETIME"))
)
