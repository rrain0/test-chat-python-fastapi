from typing import Annotated
from uuid import UUID

from pydantic import PlainSerializer


# Serialize UUID to str and vice versa
UuidAsStr = Annotated[
    UUID,
    PlainSerializer(
        lambda v: str(v),
        return_type=str
    )
]
