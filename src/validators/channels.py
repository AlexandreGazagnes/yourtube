from pydantic import BaseModel
from src.helpers import make_now, make_token


class ChannelBase(BaseModel):
    id_channel: str = ""
    name: str
    interest: float = 2.5
    date: str = make_now()
    id_language: str
    id_categ_1: str


default_channel = ChannelBase(
    id_channel=make_token(4),
    name=make_token(4),
    id_language="En",
    id_categ_1="Misc.",
)


class Channel:
    base = ChannelBase
    default = default_channel
