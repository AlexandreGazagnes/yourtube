from sqlalchemy import text
from src.db import Session, engine

# from src.queries. import VideoQuery

# from src.queries.videos import query_all_videos


def query_all(Table, engine=engine, limit: int = 300):
    """query all rows from a table"""

    with Session(engine) as session:
        result = session.query(Table).limit(limit=limit).all()
        json = [row.__dict__ for row in result]
        return json

    return []


def _perform_raw_query(query_string: str):
    """take a sql raw query and return a list of dict from the query"""

    sql_query = text(query_string)

    with Session(engine) as session:
        result = session.execute(sql_query)

    keys = result.keys()

    result = [dict(zip(keys, row)) for row in result]

    return result


class Query:
    all = query_all
    perform_raw_query = _perform_raw_query
