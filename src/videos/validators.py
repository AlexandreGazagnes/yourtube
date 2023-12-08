from pydantic import BaseModel
from src.helpers.helpers import make_now, make_token


class _VideoBase(BaseModel):
    """ """

    query: str | None = None
    skip: int = 0
    limit: int = 200
    last_days: int = 30
    duration_min: int = 3 * 60
    duration_max: int = 10 * 3600
    id_language: str | None = None
    watched: int = -1
    order_by: str = "published"
    order_direction: str = "desc"
    id_categ_0: str | None = None
    id_categ_1: str | None = None
    id_categ_2: str | None = None
    id_status: str | None = None


# _default_video = _VideoBase(
#     query=None,
#     limit=10_000,
#     last_days=10_000,
#     duration_min=3 * 60,
#     duration_max=10 * 3600,
#     id_user=None,
#     id_categ_1=None,
#     id_categ_2=None,
#     id_language=None,
#     id_status=[],
#     watched=-1,
#     order_by="published",
# )


class VideoValidator:
    base = _VideoBase
    # default = _default_video
