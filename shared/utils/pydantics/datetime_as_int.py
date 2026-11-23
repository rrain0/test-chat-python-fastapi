from datetime import datetime, timezone
from typing import Annotated

from pydantic import BeforeValidator, PlainSerializer


# Serialize datetime to int and vice versa
DatetimeAsInt = Annotated[
    datetime,
    BeforeValidator(
        lambda v: datetime.fromtimestamp(v, tz=timezone.utc) if isinstance(v, (int, float)) else v
    ),
    PlainSerializer(
        lambda v: int(v.timestamp()),
        return_type=int
    )
]
