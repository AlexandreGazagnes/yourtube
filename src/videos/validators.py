from pydantic import BaseModel
from src.helpers.helpers import make_now, make_token


class _VideoBase(BaseModel):
    query: str | None = None
    limit: int = 10_000
    last_days: int = 10_000
    duration_min: int = 3 * 60
    duration_max: int = 10 * 3600
    id_user: int | None = None
    id_categ_1: list | None = None
    id_categ_2: list | None = None
    id_language: list | None = None
    id_status: list | None = None
    watched: int = -1
    order_by: str = "published"


_default_video = _VideoBase(
    query=None,
    limit=10_000,
    last_days=10_000,
    duration_min=3 * 60,
    duration_max=10 * 3600,
    id_user=None,
    id_categ_1=None,
    id_categ_2=None,
    id_language=None,
    id_status=[],
    watched=-1,
    order_by="published",
)


class VideoValidator:
    base = _VideoBase
    default = _default_video
