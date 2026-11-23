from pydantic import BaseModel

from shared.utils.pydantics.datetime_as_iso_z import DatetimeAsIsoZ
from shared.utils.pydantics.uuid_as_string import UuidAsStr


class RdWebSessionByToken(BaseModel):
    id: UuidAsStr
    created_at: DatetimeAsIsoZ
    refresh_token_id: UuidAsStr
    refresh_token_created_at: DatetimeAsIsoZ
    refresh_token_expires_at: DatetimeAsIsoZ
    user_id: UuidAsStr
    last_active_at: DatetimeAsIsoZ
    last_active_at_ip: str | None
    last_active_at_device: str | None
