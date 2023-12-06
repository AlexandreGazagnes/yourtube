import logging

# from src.videos.models.db import Session, engine
from src.videos.models import Video

from src.helpers.helpers import make_time_delta
from src.db import Session, engine

from src.channels.models import Channel
from src.userschannels.models import UserChannel
from sqlalchemy.sql import text

import pandas as pd


def _query_user_counts():
    pass


def _query_all_id_users():
    pass


def _pre_query_preferences(
    id_user: str,
) -> dict[str:list]:
    """get user preferences from db and return as json as list
    of unique values for each field"""

    query_string = f""" 
        select 	uc.id_user,
                c.author,
                c.id_channel,
                c.id_channel,
                c.id_language,
                cc.id_categ_1,
                cc.id_categ_2
        from userschannels uc
        left join channels c on c.id_channel = uc.id_channel
        left join categ_1 cc on cc.id_categ_1 = c.id_categ_1
        where uc.id_user = 3;
    """

    sql_query = text(query_string)

    with Session(engine) as session:
        result = session.execute(sql_query)

    keys = result.keys()

    result = [dict(zip(keys, row)) for row in result]

    df = pd.DataFrame(result)

    json = {k: df[k].unique().tolist() for k in df.columns}
    return json


def _pre_query_channels(
    id_channel_list: list[str],
) -> list[dict]:
    """for a list of query  retrun list of dict of channels info"""

    query_string = f""" 
        select  c.id_channel,
                c.name,
                c.author,
                c.interest,
                c.thumbnail_channel_url,
                c.id_language,
                c.id_categ_1,
                cc.id_categ_2
        from channels c
        left join categ_1 cc on c.id_categ_1 = cc.id_categ_1
        where c.id_channel in {tuple(id_channel_list)};
    """

    sql_query = text(query_string)

    with Session(engine) as session:
        result = session.execute(sql_query)

    keys = result.keys()
    result = [dict(zip(keys, row)) for row in result]

    # df = pd.DataFrame(result)

    # json = {k: df[k].unique().tolist() for k in df.columns}
    # return json

    return result


def _pre_query_last_videos(id_channel: str, limit: int = 5) -> list[dict]:
    """for a channel id return last videos limit 10 order by published desc"""

    query_string = f"""
        select  v.id_video,
                v.title,
                v.duration,
                v.id_channel,
                v.published,
                v.thumbnail_video_url,
                v.views,
                v.stars, 
                v.votes,
                v.thumbnail_video_url,
                c.id_language,
                c.name, 
                c.author,
                c.thumbnail_channel_url,
                cc.id_categ_1,
                cc.id_categ_2
        from videos v
        left join channels c on c.id_channel = v.id_channel
        left join categ_1 cc on cc.id_categ_1 = v.id_categ_1
        where v.id_channel = '{id_channel}'
        order by v.published desc
        limit {limit};
        """

    sql_query = text(query_string)

    with Session(engine) as session:
        result = session.execute(sql_query)

    keys = result.keys()
    result = [dict(zip(keys, row)) for row in result]

    # for k, v in result.items():
    for i, v in enumerate(result):
        result[i]["published"] = str(v["published"])

    return result


def _query_preferences(id_user: str, limit: int = 5):
    """get user preferences from db and return as json"""

    # main preferences
    json = _pre_query_preferences(id_user=id_user)

    # list of channels with details
    json["channels"] = _pre_query_channels(id_channel_list=json["id_channel"])

    # for each channel add last videos
    for i, channel in enumerate(json["channels"]):
        id_channel = channel["id_channel"]
        json["channels"][i]["last_videos"] = _pre_query_last_videos(
            id_channel=id_channel
        )

    # TODO add n last videos, n best videos, n most votes videos

    return json


class UserQuery:
    counts = _query_user_counts
    all_id_users = _query_all_id_users
    preferences = _query_preferences


# video_item = {
#     "title": "",
#     "duration": "",
#     "channel_id": "",
#     "cahnnel_name": "",
#     "channel_author": "",
#     "image_url": "",
#     "published": "",
#     "views": "",
#     "loves": "",
#     "id_categ_1": "",
#     "id_categ_2": "",
#     "id_language": "",
# }


# channel_item = {
#     "name": "name",
#     "author": "author",
#     "image": "image",
#     "last_videos": [video_item, video_item],
#     "id_categ_1": "id_categ_1",
#     "id_categ_2": "id_categ_2",
#     "id_language": "id_language",
# }


# payload = {
#     "id_user": [1],
#     "id_language": [1, 2, 3],
#     "id_categ_1": [1, 2, 3],
#     "id_categ_2": [1, 2, 3],
#     "channels": [{channel_item, channel_item, channel_item}],
# }
