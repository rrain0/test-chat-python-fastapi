from datetime import datetime
from typing import Annotated

from pydantic import BeforeValidator, PlainSerializer

from shared.utils.datetimes.datetime_to_iso_z import datetime_to_iso_z


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
