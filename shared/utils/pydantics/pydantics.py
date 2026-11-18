from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID

from pydantic import BeforeValidator, PlainSerializer

from shared.utils.datetimes.datetime_to_iso_z import datetime_to_iso_z


# Serialize UUID to str and vice versa
UuidAsStr = Annotated[
    UUID,
    PlainSerializer(
        lambda v: str(v),
        return_type=str
    )
]


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


# Serialize datetime to yyyy-MM-ddThh:mm:ss.SSSZ and vice versa
DatetimeAsIsoZ = Annotated[
    datetime,
    BeforeValidator(
        lambda v: datetime.fromisoformat(v) if isinstance(v, str) else v
    ),
    PlainSerializer(
        lambda v: datetime_to_iso_z(v),
        return_type=str
    )
]
