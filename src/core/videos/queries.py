import logging

from sqlalchemy.sql import text

from src.db import Session, engine
from src.db import Db
from src.params import get_params, params


def query_one(id_video: str, id_channel: str, engine=None) -> dict:
    """Query one video by id_video"""

    # engine
    if not engine:
        engine = Db.engine(get_params("dev"))

    # query_string
    query_string = f"""
    SELECT v.title, v.id_video, c.author, c.id_channel, c.name, c.id_categ_1 
    FROM videos v 
    LEFT JOIN channels c ON v.id_channel = c.id_channel
    WHERE v.id_video like '{id_video}'
    ;
    """

    sql_query = text(query_string)

    try:
        with Session(engine) as session:
            result = session.execute(sql_query)
    except Exception as e:
        logging.error(f"error in query: {e} for id_video: {id_video}")
        return {}

    try:
        keys = result.keys()
        result = [dict(zip(keys, row)) for row in result]
    except Exception as e:
        logging.error(f"error in query results: {e} for id_video: {id_video}")
        return {}

    if not len(result):
        logging.error(f"no results for id_video: {id_video}")
        return {}

    return result[0]
