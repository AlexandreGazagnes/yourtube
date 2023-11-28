import logging, time, random

# from fastapi import FastAPI, HTTPException, APIRouter, Depends


# from src.db import Channel, Video, session, engine, Session

# from src.helpers.routers import jsonify, validate_token  # token_required
from src.home.helpers import HomeHelpers

# from src.queries import query_all, jsonify
# from src.validators import ChannelBase, default_channel
# import pandas as pd

# from src.videos.models import Video
# from src.videos.queries import VideoQuery
# from src.helpers.queries import query_all

# logging.basicConfig(level=logging.INFO)


def _update():
    """ """
    T0 = time.time(), time.time()

    # channel list ids and old videos
    channel_list_ids, time_load_channels = HomeHelpers.load_channels_ids()
    old_videos_ids, time_load_videos = HomeHelpers.load_old_videos_ids()

    # feeds new videos
    new_videos, time_get_feeds = HomeHelpers.load_feeds(channel_list_ids)
    new_videos = HomeHelpers.clean_new_videos(new_videos)

    # payload
    payload = HomeHelpers.make_payload()
    payload["old_videos_count"] = len(old_videos_ids)
    payload["new_videos_count"] = len(new_videos)
    payload["time_load_channels"] = time_load_channels
    payload["time_load_videos"] = time_load_videos
    payload["time_get_feeds"] = time_get_feeds

    # add update
    payload = HomeHelpers.add_update_db(
        new_videos=new_videos,
        old_videos_ids=old_videos_ids,
        payload=payload,
    )

    payload = HomeHelpers.reshape_payload(payload, T0)


class HomeFunctions:
    update = _update
