import logging

from src.channels.models import Channel

from src.helpers.queries import _perform_raw_query
from src.db import Session, engine


###################
#   CHANNEL
##################


def _query_channel_by_id(id_channel: str):
    """Return channel by id_channel"""

    with Session(engine) as session:
        result = session.query(Channel).filter_by(id_channel=id_channel).first()

    if not result:
        logging.error(f"channel not found: {id_channel}")
        return {"message": "channel not found"}

    logging.warning(result.to_dict())
    result = result.to_dict()

    return result


##################
#   CHANNELS
##################


def _query_all_channels():
    """Return all channels"""

    with Session(engine) as session:
        results = session.query(Channel).all()
    results = [channel.dict() for channel in results]

    return results, len(results)


def _query_channels_by_user(
    id_user: int,
    limit: int | None = None,
    skip: int | None = None,
    order_by: str = "id_channel",
    order_direction: str = "desc",
):
    """Return all channels by user"""

    order_by = "c.id_channel"

    query_string = f"""
        SELECT c.id_channel, c.name, c.channel_description, c.created_at, c.updated_at, c.id_language, c.id_categ_1
        FROM userschannels uc 
        LEFT JOIN channels c ON c.id_channel = uc.id_channel
        WHERE uc.id_user = {id_user}
        ORDER BY {order_by} {order_direction}
        {"LIMIT " + str(limit) if limit else ""}
        ;
        """

    logging.info(query_string)

    resuts = _perform_raw_query(query_string)

    logging.info(resuts)

    return resuts


def _query_channel_all_id():
    """Return all id_channel"""

    with Session(engine) as session:
        results = session.query(Channel.id_channel).all()

    results = [result[0] for result in results]

    return list(set(results))


class ChannelQueries:
    """ """

    by_id_channel = _query_channel_by_id


class ChannelsQueries:
    """channels queries"""

    all = _query_all_channels
    all_id = _query_channel_all_id
    by_user = _query_channels_by_user
