from src.models.db import Session, engine
from src.queries.videos import VideoQuery

# from src.queries.videos import query_all_videos


def query_all(Table, engine=engine, limit: int = 300):
    """query all rows from a table"""

    with Session(engine) as session:
        result = session.query(Table).limit(limit=limit).all()
        json = [row.__dict__ for row in result]
        return json

    return []


class Query:
    all = query_all
    videos = VideoQuery

