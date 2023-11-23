from src.models.db import Session, engine


def query_all(Table, engine=engine):
    """query all rows from a table"""

    with Session(engine) as session:
        result = session.query(Table).all()
        json = [row.__dict__ for row in result]

        return json
    return []
