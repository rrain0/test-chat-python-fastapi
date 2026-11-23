from typing import Annotated

from pydantic import BeforeValidator, PlainSerializer


# Serialize int to str and vice versa
IntAsStr = Annotated[
    int,
    BeforeValidator(
        lambda v: int(v) if isinstance(v, str) else v
    ),
    PlainSerializer(
        lambda v: str(v),
        return_type=str
    )
]
