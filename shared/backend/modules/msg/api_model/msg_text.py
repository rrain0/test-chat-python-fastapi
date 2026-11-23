from pydantic import BaseModel


class BackApiMsgText(BaseModel):
    msg_text: str
