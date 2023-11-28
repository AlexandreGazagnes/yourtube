from src.models.db import Session, engine
from src.models.db import Videos, Channels

from src.helpers import make_time_delta


def _query_all_videos(
    limit: int = 10_000,
    last_days: int = 10_000,
):
    """query all rows from a table"""

    with Session(engine) as session:
        result = (
            session.query(Videos)
            .order_by(Videos.published.desc())
            .filter(Videos.published >= make_time_delta(last_days))
            .limit(limit)
            .all()
        )

        json = [row.__dict__ for row in result]

        return json
    return []


def _querry_all_id_videos(limit: int = 10_000, last_days: int = 10_000):
    with Session(engine) as session:
        result = session.query(Videos.id_video).all()
        result = [row[0].strip() for row in result]
        return list(set(result))

    return []


def _query_by_categ_1():
    pass


def _query_by_categ_2():
    pass


def _query_by_language():
    pass


def _query_by_status():
    pass


def _query_by_watched():
    pass


def _query_by_channel():
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


if __name__ == "__main__":
    print(VideoQuery.all())
    print(len(VideoQuery.all()))

    #

    _query_all_videos(limit=10, last_days=1)

