from pydantic import BaseModel
from src.helpers.helpers import make_now, make_token


class _VideoBase(BaseModel):
    id_video: str = ""
    title: str
    author: str
    name: str
    published: str
    stars: float
    views: int
    id_channel: str
    watched: int = 0
    id_status: str = "none"


_default_video = _VideoBase(
    id_video=make_token(4),
    title=make_token(4),
    author=make_token(4),
    name=make_token(4),
    published=make_now(),
    stars=0.0,
    views=0,
    id_channel="",
    watched=0,
    id_status="none",
)


class VideoValidator:
    base = _VideoBase
    default = _default_video
