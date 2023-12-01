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


def _query_preferences(
    id_user: str,
):
    query_string = f""" 
    select 
                v.category,
                u.id_user,
                cc.id_categ_1,
                cc.id_categ_2, 
                cc.id_language,

    from videos v
    left join userschannels u on u.id_channel = v.id_channel
    left join channels c on c.id_channel = v.id_channel
    left join categ_1 cc on cc.id_categ_1 = c.id_categ_1
    where u.id_user = {id_user};
    """

    sql_query = text(query_string)

    with Session(engine) as session:
        result = session.execute(sql_query)

    keys = result.keys()

    result = [dict(zip(keys, row)) for row in result]

    df = pd.DataFrame(result)

    json = {k: df[k].unique().tolist() for k in df.columns}

    return json


class UserQuery:
    counts = _query_user_counts
    all_id_users = _query_all_id_users
    preferences = _query_preferences
