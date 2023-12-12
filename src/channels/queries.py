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
        return {}

    logging.warning(result.to_dict())
    result = result.to_dict()

    return result


##################
#   CHANNELS
##################


def _query_all_ids_channels():
    """Return all id_channel"""

    with Session(engine) as session:
        results = session.query(Channel.id_channel).all()

    results = [result[0] for result in results]

    return list(set(results)), len(results)


def _query_all_channels(
    limit: int = 10_000,
    skip: int = 0,
    order_by: str | None = None,
    order_direction: str = "desc",
):
    """Return all channels"""

    with Session(engine) as session:
        results = session.query(Channel).all()
    results = [channel.to_dict() for channel in results]

    total = len(results)
    results = results[skip : skip + limit]

    return results, total


def _query_channels_by_user(
    id_user: int,
    limit: int | None = 1_000,
    skip: int | None = 0,
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
        ;
        """

    logging.info(query_string)

    resuts = _perform_raw_query(query_string)

    # to be investigated
    # resuts = [result.to_dict() for result in resuts]

    total = len(resuts)
    resuts = resuts[skip : skip + limit]

    logging.info(resuts)

    return resuts, total


def _query_channels_by_categ_1(
    id_user: int,
    limit=1_000,
    skip: int = 0,
    order_by=None,
    order_direction: str | None = None,
) -> dict[str : list[dict]]:
    """Return all channels by user"""

    # query
    query_string = f"""select c.id_channel, c.name, c.author, 
    c.channel_description, c.created_at, c.updated_at, c.id_language, 
    c.id_categ_1, c.thumbnail_channel_url
    from userschannels uc
    left join channels c on c.id_channel = uc.id_channel
    where uc.id_user = {id_user}
    ;
    """

    logging.info(query_string)

    # gloabl query
    resuts = _perform_raw_query(query_string)

    # to be investigated
    # resuts = [result.to_dict() for result in resuts]

    # update
    total = len(resuts)
    resuts = resuts[skip : skip + limit]

    # list unique id_categ_1 of results
    categ_1_list = [result["id_categ_1"] for result in resuts]
    categ_1_list = list(set(categ_1_list))

    # resttuct data in dict of list
    categ_1_dict = {categ_1: [] for categ_1 in categ_1_list}
    for result in resuts:
        categ_1_dict[result["id_categ_1"]].append(result)

    logging.info(categ_1_dict)

    return categ_1_dict, total


class ChannelQuery:
    """ """

    # renommer en get tout court
    by_id_channel = _query_channel_by_id


class ChannelsQueries:
    """channels queries"""

    all = _query_all_channels
    all_ids = _query_all_ids_channels
    by_user = _query_channels_by_user
    by_categ_1 = _query_channels_by_categ_1
