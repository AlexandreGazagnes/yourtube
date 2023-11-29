import logging, time, random


import os, sys, logging, time, random
from src.db import Session, engine

from src.videos.models import Video
from src.videos.queries import VideoQuery

from src.channels.models import Channel
from src.core.thumbnails import enhance_video
from src.helpers.queries import query_all

from src.channels.queries import ChannelQuery
from src.core.feeds import extract_rss, extract_rss_and_flatten
from src.core.thumbnails import enhance_video
from src.helpers.helpers import make_now

from src.videos.queries import VideoQuery
from random import shuffle
from src.helpers.helpers import make_now

# from fastapi import FastAPI, HTTPException, APIRouter, Depends


# from src.db import Channel, Video, session, engine, Session

# from src.helpers.routers import jsonify, validate_token  # token_required
from src.home.helpers import HomeHelpers
from src.core.thumbnails import enhance_video

# from src.queries import query_all, jsonify
# from src.validators import ChannelBase, default_channel
# import pandas as pd

# from src.videos.models import Video
# from src.videos.queries import VideoQuery
# from src.helpers.queries import query_all

# logging.basicConfig(level=logging.INFO)


def _update(
    new=True,
    old=True,
    random_=True,
):
    """Update the database with new videos and old videos"""

    T0 = time.time()

    # channel list ids and old videos
    channel_list_ids, time_load_channels = HomeHelpers.load_channels_ids()
    old_videos_ids, time_load_videos = HomeHelpers.load_old_videos_ids()

    # feeds new videos
    new_videos, time_get_feeds = HomeHelpers.load_feeds(channel_list_ids)
    new_videos = HomeHelpers.clean_videos(new_videos)

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
        new=new,
        old=old,
        random_=random_,
    )

    payload = HomeHelpers.reshape_payload(payload, T0)
    return payload


def _fix_old_videos():
    """Fix data inconsistant default values for old videos"""

    broken_videos = HomeHelpers.get_broken_videos()
    broken_videos = HomeFunctions.clean_videos(broken_videos)

    for i, video in enumerate(broken_videos):
        # enhance video
        try:
            video = enhance_video(video)
        except Exception as e:
            logging.error(f"enhance video - {e} - {video}")
            continue

        # update video
        id_video = video["id_video"]
        video["updated_at"] = make_now()

        # add in db
        try:
            with Session(engine) as session:
                session.query(Video).filter_by(id_video=id_video).update(video)
                session.commit()
                # payload["updated"] += 1
        except Exception as e:
            logging.error(f"update video - {e} - {video}")
            # payload["errors_updated"] += 1

    payload = {"ok": True}
    return payload


class HomeFunctions:
    update = _update
    fix = _fix_old_videos
