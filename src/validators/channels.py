from pydantic import BaseModel
from src.helpers import make_now, make_token


class _ChannelBase(BaseModel):
    id_channel: str = ""
    name: str
    interest: float = 2.5
    date: str = make_now()
    id_language: str
    id_categ_1: str


_default_channel = _ChannelBase(
    id_channel=make_token(4),
    name=make_token(4),
    id_language="En",
    id_categ_1="Misc.",
)


class ChannelValidator:
    base = _ChannelBase
    default = _default_channel
