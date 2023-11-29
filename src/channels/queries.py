from src.channels.models import Channel

from src.db import Session, engine


def _query_all():
    """Return all channels"""

    with Session(engine) as session:
        results = session.query(Channel).all()
    results = [channel.dict() for channel in results]
    return results


def _query_all_id_channel():
    """Return all id_channel"""

    with Session(engine) as session:
        results = session.query(Channel.id_channel).all()
    results = [result[0] for result in results]
    return list(set(results))


class ChannelQuery:
    all = _query_all
    all_id_channel = _query_all_id_channel
