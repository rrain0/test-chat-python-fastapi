from pydantic import BaseModel, ConfigDict, Field

from shared.utils.pydantics.pydantics import UuidAsStr, DatetimeAsInt


class TgBotSessionToken(BaseModel):
    # Configure model to enforce alias mapping everywhere by default
    model_config = ConfigDict(
        populate_by_name=True,   # Allows instantiating with either user_id or sub
        serialize_by_alias=True,  # Forces model_dump() to output 'sub' and 'exp' automatically
    )

    type: str
    id: UuidAsStr
    created_at: DatetimeAsInt = Field(alias='iat')
    expires_at: DatetimeAsInt = Field(alias='exp')
    session_id: UuidAsStr
    user_id: UuidAsStr = Field(alias='sub')
    user_username: str
    tg_user_id: UuidAsStr
    tg_user_username: str
