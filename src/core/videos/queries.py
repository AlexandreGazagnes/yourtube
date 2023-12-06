import logging

from sqlalchemy.sql import text

from src.db import Session, engine
from src.db import Db
from src.params import get_params, params


def query_one(id_channel: str, engine=None) -> dict:
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
