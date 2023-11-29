# from src.videos.models.db import Session, engine
from src.videos.models import Video

from src.helpers.helpers import make_time_delta
from src.db import Session, engine

from src.channels.models import Channel
from src.userschannels.models import UserChannel
from sqlalchemy.sql import text


def _query_all_videos(
    limit: int = 10_000,
    last_days: int = 10_000,
    duration_min: int = 3 * 60,
    duration_max: int = 10 * 3600,
    categ_1: list = None,
    language: list = None,
    status: list = None,
    watched: int = -1,
    order_by: str = "published",
    # order: str = "desc",
):
    """query all rows from a table"""

    with Session(engine) as session:
        result = (
            session.query(Video)
            .filter(Video.published >= make_time_delta(last_days))
            .filter(Video.duration > duration_min)
            .filter(Video.duration < duration_max)
            .order_by(getattr(Video, order_by).desc())
            .limit(limit)
            .all()
        )

        # .order_by(Video.published.desc()
        json = [row.__dict__ for row in result]

        return json
    return []


def _querry_all_id_videos(limit: int = 10_000, last_days: int = 10_000):
    with Session(engine) as session:
        result = session.query(Video.id_video).all()
        result = [row[0].strip() for row in result]
        return list(set(result))

    return []


def _count():
    with Session(engine) as session:
        result = session.query(Video).count()
        return result


def _query_by_user(
    id_user: str,
    limit: int = 10_000,
    last_days: int = 10_000,
    duration_min: int = 3 * 60,
    duration_max: int = 10 * 3600,
    categ_1: list = None,
    language: list = None,
    status: list = None,
    watched: int = -1,
    order_by: str = "published",
    # order: str = "desc",
):
    """ """

    # Example query
    # query_string = f"""
    #             select *
    #             from videos v
    #             left join userschannels u on u.id_channel = v.id_channel
    #             where u.id_user = {id_user};
    #             """

    # sql_query = text(query_string)

    # with Session(engine) as session:
    #     result = session.execute(sql_query)

    with Session(engine) as session:
        result = (
            session.query(Video, UserChannel)
            .leftjoin(UserChannel, Video.id_channel == UserChannel.id_channel)
            .filter(UserChannel.id_user == id_user)
            .filter(Video.published >= make_time_delta(last_days))
            .filter(Video.duration > duration_min)
            .filter(Video.duration < duration_max)
            .order_by(getattr(Video, order_by).desc())
            .limit(limit)
            .all()
        )

        json = [row.__dict__ for row in result]

        return json
    return []


def _query_by_categ_1(
    categ_1: list,
    limit: int = 10_000,
    last_days: int = 10_000,
    short_videos: bool = False,
    language: list = None,
    status: list = None,
    watched: int = -1,
):
    pass


def _query_by_categ_2(
    categ_2: list,
    limit: int = 10_000,
    last_days: int = 10_000,
    short_videos: bool = False,
    language: list = None,
    status: list = None,
    watched: int = -1,
):
    pass


def _query_by_language(
    language: list,
    limit: int = 10_000,
    last_days: int = 10_000,
    categ_1: list = None,
    short_videos: bool = False,
    status: list = None,
    watched: int = -1,
):
    pass


def _query_by_status(
    status: list,
    limit: int = 10_000,
    last_days: int = 10_000,
    short_videos: bool = False,
    categ_1: list = None,
    language: list = None,
    watched: int = -1,
):
    pass


def _query_by_watched(
    watched: int,
    id_user: str,
    limit: int = 10_000,
    last_days: int = 10_000,
    short_videos: bool = False,
    categ_1: list = None,
    language: list = None,
    status: list = None,
):
    pass


def _query_by_channel(
    id_channel: str,
    limit: int = 10_000,
    last_days: int = 10_000,
    short_videos: bool = False,
    categ_1: list = None,
    language: list = None,
    status: list = None,
    watched: int = -1,
):
    pass


class VideoQuery:
    all = _query_all_videos
    by_categ_1 = _query_by_categ_1
    by_categ_2 = _query_by_categ_2
    by_language = _query_by_language
    by_status = _query_by_status
    by_watched = _query_by_watched
    by_channel = _query_by_channel
    all_id_videos = _querry_all_id_videos
    count = _count
    by_user = _query_by_user


# if __name__ == "__main__":
#     print(VideoQuery.all())
#     print(len(VideoQuery.all()))

#     #

#     _query_all_videos(limit=10, last_days=1)
