import logging


from fastapi import HTTPException

from sqlalchemy.sql import text

from src.channels.models import Channel
from src.userschannels.models import UserChannel
from src.languages.models import Language

from src.videos.validators import VideoValidator
from src.helpers.queries import Query
from src.categ_1.models import Categ1

# from src.videos.models.db import Session, engine
from src.videos.models import Video
from src.helpers.helpers import make_time_delta

from src.db import Session, engine
from src.helpers.helpers import stringify_duration


base_fields = "v.title, v.category, v.thumbnail_video_url, v.published, \
v.duration, v.views, v.id_video, v.keywords, v.stars, v.id_channel, \
v.votes, v.id_categ_0, c.id_channel, c.thumbnail_channel_url, c.name,\
c.author, c.id_language, c.id_categ_1, cc.id_categ_2 "


# def _clean_duration(video_dict: list):
#     """clean duration from seconds to string"""

#     video_dict["duration"] = stringify_duration(video_dict["duration"])
#     return video_dict


# def _extra_filter_query(
#     result: list,
#     query: str | None = None,
#     id_language: str | None = None,
#     id_categ_1: str | None = None,
# ):
#     """ """

#     # filter by query
#     if query and isinstance(query, str):
#         # filter tiltle by query
#         result = [i for i in result if query.strip().lower() in i["title"].lower()]
#         # result = [_clean_duration(i) for i in result]

#         return result

#     # filter by language
#     if id_language and isinstance(id_language, str):
#         # get all language keys
#         with Session(engine) as session:
#             language_list = session.query(Language.id_language).all()
#             language_list = [i[0] for i in language_list]
#         # if not good raise error
#         if id_language not in language_list:
#             raise HTTPException(
#                 status_code=500,
#                 detail=f"language {id_language} not found, should be in {language_list}",
#             )
#         # do filter
#         result = [i for i in result if i["id_language"] == id_language]

#     # filter by id_categ_1
#     if id_categ_1 and isinstance(id_categ_1, str):
#         # get all categ1 keys
#         with Session(engine) as session:
#             categ1_list = session.query(Categ1.id_categ_1).all()
#             categ1_list = [i[0] for i in categ1_list]
#         # if not good raise error
#         if id_categ_1 not in categ1_list:
#             raise HTTPException(
#                 status_code=500,
#                 detail=f"categ1 {id_categ_1} not found, should be in {categ1_list}",
#             )
#         # do filter
#         result = [i for i in result if i["id_categ_1"] == id_categ_1]

#     return result


def _prepare_query(query: str | None = None):
    """lower stip and remove accent if needed"""

    query = query.strip().lower() if query else ""

    query = (
        query.replace("é", "e")
        .replace("è", "e")
        .replace("ê", "e")
        .replace("ë", "e")
        .replace("à", "a")
        .replace("â", "a")
        .replace("ä", "a")
        .replace("ù", "u")
        .replace("û", "u")
        .replace("ü", "u")
        .replace("î", "i")
        .replace("ï", "i")
        .replace("ô", "o")
        .replace("ö", "o")
        .replace("ç", "c")
        .replace("œ", "oe")
        .replace("æ", "ae")
        .replace("ÿ", "y")
        .replace("ñ", "n")
        # .replace(" ", "%") ==> why not
    )
    return query


#################################
#   VIDEO
#################################


def _query_video_by_id(id_video: str):
    """query video by id_video"""

    with Session(engine) as session:
        result = session.query(Video).filter_by(id_video=id_video).first()

    if not result:
        logging.error(f"video not found: {id_video}")
        return {"message": "video not found"}

    logging.warning(result.to_dict())
    result = result.to_dict()

    return result


#################################
#   VIDEOS
#################################


def _query_videos_count():
    """count all rows from a table"""

    with Session(engine) as session:
        result = session.query(Video).count()

    return result


def _query_all_ids_videos(
    limit: int = 10_000,
    last_days: int = 10_000,
):
    """query all id_videos from a table"""

    with Session(engine) as session:
        result = session.query(Video.id_video).all()

    result = [row[0].strip() for row in result]
    return list(set(result))


def _query_all_videos(
    query: str | None = None,
    skip: int = 0,
    limit: int = 200,
    days_min: int = 0,
    days_max: int = 30,
    duration_min: int = 3 * 60,
    duration_max: int = 10 * 3600,
    id_language: str | None = None,
    watched: int = -1,
    order_by: str = "published",
    order_direction: str = "desc",
    id_categ_0: str | None = None,
    id_categ_1: str | None = None,
    id_categ_2: str | None = None,
    id_status: str | None = None,
):
    """query all rows from a table"""

    query_string = f"""
                select {base_fields} 
                from videos v
                left join channels c on c.id_channel = v.id_channel
                left join categ_1 cc on cc.id_categ_1 = c.id_categ_1
                where v.published   >= '{make_time_delta(days_max)}'
                and v.published <= '{make_time_delta(days_min)}'
                and v.duration > {duration_min}
                and v.duration < {duration_max}
                {f"and v.id_categ_0 like '{id_categ_0}'" if id_categ_0 else ""}
                {f"and c.id_categ_1 like '{id_categ_1}'" if id_categ_1 else ""}
                {f"and cc.id_categ_2 like '{id_categ_2}'" if id_categ_2 else ""}
                {f"and c.id_language like '{id_language}'" if id_language else ""}
                {f"and v.title like '%{_prepare_query(query)}%'" if query else ""}
                order by v.{order_by} {order_direction}
                ;
                """

    # limit {limit};

    logging.warning(query_string)

    result = Query.perform_raw_query(query_string)
    total = len(result)
    result = result[skip : skip + limit]

    return result, total


def _query_videos_by_user(
    id_user: int,
    query: str | None = None,
    skip: int = 0,
    limit: int = 200,
    days_min: int = 0,
    days_max: int = 30,
    duration_min: int = 3 * 60,
    duration_max: int = 10 * 3600,
    id_language: str | None = None,
    watched: int = -1,
    order_by: str = "published",
    order_direction: str = "desc",
    id_categ_0: str | None = None,
    id_categ_1: str | None = None,
    id_categ_2: str | None = None,
    id_status: str | None = None,
):
    """query all rows from a user"""

    query_string = f"""
                select {base_fields}
                from videos v
                left join userschannels u on u.id_channel = v.id_channel
                left join channels c on c.id_channel = v.id_channel
                left join categ_1 cc on cc.id_categ_1 = c.id_categ_1
                where u.id_user = {id_user}
                and v.published   >= '{make_time_delta(days_max)}'
                and v.published <= '{make_time_delta(days_min)}'
                and v.duration > {duration_min}
                and v.duration < {duration_max}
                {f"and v.id_categ_0 like '{id_categ_0}'" if id_categ_0 else ""}
                {f"and c.id_categ_1 like '{id_categ_1}'" if id_categ_1 else ""}
                {f"and cc.id_categ_2 like '{id_categ_2}'" if id_categ_2 else ""}
                {f"and c.id_language like '{id_language}'" if id_language else ""}
                {f"and v.title like '%{_prepare_query(query)}%'" if query else ""}
                {f"and v.id_status like '{id_status}'" if id_status else ""}
                order by v.{order_by} {order_direction}
                ;
                """  #                 limit {limit};

    logging.warning(query_string)

    result = Query.perform_raw_query(query_string)
    total = len(result)
    result = result[skip : skip + limit]

    return result, total


def _query_videos_by_channel(
    id_channel: int,
    query: str | None = None,
    skip: int = 0,
    limit: int = 200,
    days_min: int = 0,
    days_max: int = 30,
    duration_min: int = 3 * 60,
    duration_max: int = 10 * 3600,
    id_language: str | None = None,
    watched: int = -1,
    order_by: str = "published",
    order_direction: str = "desc",
    id_categ_0: str | None = None,
    id_categ_1: str | None = None,
    id_categ_2: str | None = None,
    id_status: str | None = None,
):
    """query all rows from a user"""

    query_string = f"""
                select {base_fields}
                from videos v
                left join channels c on c.id_channel = v.id_channel
                left join categ_1 cc on cc.id_categ_1 = c.id_categ_1
                where c.id_channel like '{id_channel}'
                and v.published   >= '{make_time_delta(days_max)}'
                and v.published <= '{make_time_delta(days_min)}'
                and v.duration > {duration_min}
                and v.duration < {duration_max}
                {f"and v.id_categ_0 like '{id_categ_0}'" if id_categ_0 else ""}
                {f"and c.id_categ_1 like '{id_categ_1}'" if id_categ_1 else ""}
                {f"and cc.id_categ_2 like '{id_categ_2}'" if id_categ_2 else ""}
                {f"and c.id_language like '{id_language}'" if id_language else ""}
                {f"and v.title like '%{_prepare_query(query)}%'" if query else ""}
                order by v.{order_by} {order_direction}
                ;
                """  #                 limit {limit};

    logging.warning(query_string)

    result = Query.perform_raw_query(query_string)
    total = len(result)
    result = result[skip : skip + limit]

    return result, total


class VideoQuery:
    """ """

    # renommer en get
    by_id_video = _query_video_by_id


class VideosQueries:
    """ """

    count = _query_videos_count
    all_ids = _query_all_ids_videos
    all = _query_all_videos
    by_user = _query_videos_by_user
    by_channel = _query_videos_by_channel

    # by_categ_1 = _query_by_categ_1
    # by_categ_2 = _query_by_categ_2
    # by_language = _query_by_language
    # by_status = _query_by_status
    # by_watched = _query_by_watched
