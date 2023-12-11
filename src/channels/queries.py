from src.channels.models import Channel

from src.db import Session, engine


def _query_all_channels():
    """Return all channels"""

    with Session(engine) as session:
        results = session.query(Channel).all()
    results = [channel.dict() for channel in results]

    return results, len(results)


def _query_channel_by_id(id_channel: str):
    """Return channel by id_channel"""

    with Session(engine) as session:
        result = session.query(Channel).filter_by(id_channel=id_channel).first()

    result = result.dict()

    return result


def _query_channel_all_id():
    """Return all id_channel"""

    with Session(engine) as session:
        results = session.query(Channel.id_channel).all()

    results = [result[0] for result in results]

    return list(set(results))


class ChannelQuery:
    """ """

    all = _query_channel_all_id
    all_id = _query_channel_all_id
    by_id_channel = _query_channel_by_id
