from pydantic import BaseModel, ConfigDict, Field

from shared.utils.pydantics.datetime_as_int import DatetimeAsInt
from shared.utils.pydantics.int_as_str import IntAsStr
from shared.utils.pydantics.uuid_as_string import UuidAsStr


class TgBotAccessToken(BaseModel):
    # Configure model to enforce alias mapping everywhere by default
    model_config = ConfigDict(
        populate_by_name=True,   # Allows instantiating with either user_id or sub
        serialize_by_alias=True,  # Forces model_dump() to output "sub" and "exp" automatically
    )

    type: str
    id: UuidAsStr
    created_at: DatetimeAsInt = Field(alias="iat")
    expires_at: DatetimeAsInt = Field(alias="exp")
    tg_user_id: IntAsStr = Field(alias="sub") # sub must be serialized as str
    tg_user_username: str
