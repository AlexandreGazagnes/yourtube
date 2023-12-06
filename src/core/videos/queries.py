"""
Queries module 
query the db for videos regarding core/video module ONLY
"""

import logging, os, time

from sqlalchemy.sql import text

from src.db import Session, engine
from src.db import Db

from src.params import get_params, params
from src.channels.queries import ChannelQuery
from src.videos.queries import VideoQuery


def _query_one(id_channel: str, engine=None) -> dict:
    """Query one video by id_video"""

    if not isinstance(id_channel, (str, int)):
        raise AttributeError(
            f"error type id_channel, expected (str, int), recieved {id_channel}"
        )

    # engine
    if not engine:
        engine = Db.engine(get_params("dev"))

    # query_string
    query_string = f"""
    SELECT c.author, c.id_channel, c.name, c.id_categ_1 
    FROM channels c
    WHERE c.id_channel like '{id_channel}'
    ;
    """

    sql_query = text(query_string)

    try:
        with Session(engine) as session:
            result = session.execute(sql_query)
    except Exception as e:
        logging.error(f"error in query: {e} for id_channel: {id_channel}")
        return {}

    try:
        keys = result.keys()
        result = [dict(zip(keys, row)) for row in result]
    except Exception as e:
        logging.error(f"error in query results: {e} for id_channel: {id_channel}")
        return {}

    if not len(result):
        logging.error(f"no results for id_channel: {id_channel}")
        return {}

    return result[0]


def _channels_ids() -> tuple[list[str], float]:
    """ """

    t0 = time.time()

    logging.warning("load channels")

    channel_list_ids = ChannelQuery.all_id_channel()
    channel_list_ids = [i for i in channel_list_ids if not i.lower().startswith("fake")]
    channel_list_ids = [i for i in channel_list_ids if not i.lower().startswith("test")]

    time_load_channels = round(time.time() - t0, 4)

    return channel_list_ids, time_load_channels


def _old_videos_ids() -> tuple[list[str], float]:
    """ """

    t0 = time.time()
    logging.warning("load videos")

    old_videos_ids = VideoQuery.all_id_videos()
    time_load_videos = round(time.time() - t0, 4)

    return old_videos_ids, time_load_videos


class CoreVideoQueries:
    """class for core video queries"""

    query_one = _query_one
    channels_ids = _channels_ids
    old_videos_ids = _old_videos_ids
