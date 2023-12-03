import logging

# from src.videos.models.db import Session, engine
from src.videos.models import Video
from fastapi import HTTPException

from src.helpers.helpers import make_time_delta
from src.db import Session, engine

from src.channels.models import Channel
from src.userschannels.models import UserChannel
from sqlalchemy.sql import text

from src.languages.models import Language
from src.videos.validators import VideoValidator
from src.helpers.queries import Query

from src.categ_1.models import Categ1


fields = "v.title, v.exact_url, v.category, v.thumbnail_video_url, v.published, \
    v.duration, v.views, v.id_status, v.id_video, v.author, v.keywords, v.stars, \
    v.votes, v.watched, c.thumbnail_channel_url, c.id_language, \
        cc.id_categ_1, cc.id_categ_2 "


def _extra_filter_query(
    result: list,
    query: str | None = None,
    id_language: str | None = None,
    id_categ_1: str | None = None,
):
    """ """

    # filter by query
    if query:
        result = [i for i in result if query.strip().lower() in i["title"].lower()]
        return result

    # filter by language
    if id_language:
        with Session(engine) as session:
            language_list = session.query(Language.id_language).all()
            language_list = [i[0] for i in language_list]

        if id_language not in language_list:
            raise HTTPException(
                status_code=500,
                detail=f"language {id_language} not found, should be in {language_list}",
            )

        result = [i for i in result if i["id_language"] == id_language]

    # filter by id_categ_1
    if id_categ_1:
        with Session(engine) as session:
            categ1_list = session.query(Categ1.id_categ_1).all()
            categ1_list = [i[0] for i in categ1_list]

        if id_categ_1 not in categ1_list:
            raise HTTPException(
                status_code=500,
                detail=f"categ1 {id_categ_1} not found, should be in {categ1_list}",
            )

        result = [i for i in result if i["id_categ_1"] == id_categ_1]

    return result


def _count():
    """count all rows from a table"""

    with Session(engine) as session:
        result = session.query(Video).count()
        return result


def _query_all_id_videos(
    limit: int = 10_000,
    last_days: int = 10_000,
):
    """query all id_videos from a table"""

    with Session(engine) as session:
        result = session.query(Video.id_video).all()
        result = [row[0].strip() for row in result]
        return list(set(result))

    return []


def _query_all_videos(
    query: str | None = None,
    limit: int = 10_000,
    last_days: int = 10_000,
    duration_min: int = 3 * 60,
    duration_max: int = 10 * 3600,
    id_language: str = None,
    watched: int = -1,
    order_by: str = "published",
    id_user: int = None,
    id_categ_1: list = None,
    id_categ_2: list = None,
    id_status: list = None,
    # order: str = "desc",
):
    """query all rows from a table"""

    query_string = f"""
                select {fields} 
                from videos v
                left join channels c on c.id_channel = v.id_channel
                left join categ_1 cc on cc.id_categ_1 = c.id_categ_1
                where v.published >= '{make_time_delta(last_days)}'
                and v.duration > {duration_min}
                and v.duration < {duration_max}
                order by v.{order_by} desc
                limit {limit};
                """

    result = Query.perform_raw_query(query_string)
    result = _extra_filter_query(result, query, id_language, id_categ_1)

    # logging.warning(result)
    return result


def _query_by_user(
    id_user: int,
    query: str | None = None,
    limit: int = 10_000,
    last_days: int = 10_000,
    duration_min: int = 3 * 60,
    duration_max: int = 10 * 3600,
    id_language: str = None,
    watched: int = -1,
    order_by: str = "published",
    id_categ_1: list = None,
    id_categ_2: list = None,
    id_status: list = None,
    # order: str = "desc",
):
    """ """

    if not id_user:
        logging.error(f"bad argument for  id_user  {id_user}")
        raise HTTPException(
            status_code=500,
            detail=f"bad argument for  id_user  {id_user}",
        )
    query_string = f"""
                select {fields} , u.id_user
                from videos v
                left join userschannels u on u.id_channel = v.id_channel
                left join channels c on c.id_channel = v.id_channel
                left join categ_1 cc on cc.id_categ_1 = c.id_categ_1
                where u.id_user = {id_user}
                and v.published >= '{make_time_delta(last_days)}'
                and v.duration > {duration_min}
                and v.duration < {duration_max}
                order by v.{order_by} desc
                limit {limit};
                """

    result = Query.perform_raw_query(query_string)
    result = _extra_filter_query(result, query, id_language, id_categ_1)

    # logging.warning(result)
    return result


# def _query_by_categ_1(
#     categ_1: list,
#     limit: int = 10_000,
#     last_days: int = 10_000,
#     short_videos: bool = False,
#     language: list = None,
#     status: list = None,
#     watched: int = -1,
# ):
#     pass


# def _query_by_categ_2(
#     categ_2: list,
#     limit: int = 10_000,
#     last_days: int = 10_000,
#     short_videos: bool = False,
#     language: list = None,
#     status: list = None,
#     watched: int = -1,
# ):
#     pass


# def _query_by_language(
#     language: list,
#     limit: int = 10_000,
#     last_days: int = 10_000,
#     categ_1: list = None,
#     short_videos: bool = False,
#     status: list = None,
#     watched: int = -1,
# ):
#     pass


# def _query_by_status(
#     status: list,
#     limit: int = 10_000,
#     last_days: int = 10_000,
#     short_videos: bool = False,
#     categ_1: list = None,
#     language: list = None,
#     watched: int = -1,
# ):
#     pass


# def _query_by_watched(
#     watched: int,
#     id_user: str,
#     limit: int = 10_000,
#     last_days: int = 10_000,
#     short_videos: bool = False,
#     categ_1: list = None,
#     language: list = None,
#     status: list = None,
# ):
#     pass


# def _query_by_channel(
#     id_channel: str,
#     limit: int = 10_000,
#     last_days: int = 10_000,
#     short_videos: bool = False,
#     categ_1: list = None,
#     language: list = None,
#     status: list = None,
#     watched: int = -1,
# ):
#     pass


class VideoQuery:
    count = _count
    all_id_videos = _query_all_id_videos
    all = _query_all_videos
    by_user = _query_by_user
    # by_categ_1 = _query_by_categ_1
    # by_categ_2 = _query_by_categ_2
    # by_language = _query_by_language
    # by_status = _query_by_status
    # by_watched = _query_by_watched
    # by_channel = _query_by_channel
