from fastapi import FastAPI, HTTPException, APIRouter, Depends
from src.models import *
from src.routers.helpers import jsonify
from src.queries import query_all, VideoQuery
from src.models.db import Channels, Videos, session, engine, Session
from src.core.feeds import extract_rss
import logging
import time
import pandas as pd

from src.core.thumbnails import enhance_video
from src.routers.helpers import jsonify, validate_token  # token_required
import random

# from src.queries import query_all, jsonify

# from src.validators import ChannelBase, default_channel

import logging

logging.basicConfig(level=logging.INFO)

home = APIRouter(
    prefix="",
    tags=["home"],
)


@home.get("/", status_code=200)
async def root():
    return jsonify(None, message="Hello World")


@home.get("/ping", status_code=200)
async def ping():
    return jsonify(None, message="pong")


@home.get("/state", status_code=200)
async def state():
    with Session(engine) as session:
        result = session.query(Videos).count()
    return jsonify({"video_count": result}, message="success")


@home.get("/update", status_code=200)
async def update(token: str = Depends(validate_token)):
    """ """

    t0, T0 = time.time(), time.time()

    # load channels
    logging.warning("load channels")
    with Session(engine) as session:
        channel_list = [i.get("id_channel") for i in query_all(Channels, limit=10_000)]
    channel_list = [i for i in channel_list if not i.lower().startswith("fake")]
    channel_list = [i for i in channel_list if not i.lower().startswith("test")]

    time_load_channels = round(time.time() - t0, 4)
    t0 = time.time()

    # feeds
    logging.warning("get feeds")
    feeds = [extract_rss(i) for i in channel_list]
    new_videos = []
    _ = [new_videos.extend(i) for i in feeds]
    time_get_feeds = round(time.time() - t0, 4)

    # clean video
    for i, video in enumerate(new_videos):
        # manage the id video
        if "id_video" not in video.keys():
            new_videos[i]["id_video"] = video.get("yt_videoid")
        # clean the video dict
        new_videos[i] = {
            i: j
            for i, j in new_videos[i].items()
            if i in Videos.__table__.columns.keys()
        }

    # load videos
    logging.warning("load videos")
    t0 = time.time()
    with Session(engine) as session:
        old_videos = VideoQuery.all_id_videos()

    time_load_videos = round(time.time() - t0, 4)

    # place holders
    added = 0
    updated = 0
    errors_added = 0
    errors_updated = 0
    old_videos_count = len(old_videos)
    new_videos_count = len(new_videos)

    t0 = time.time()
    logging.warning("add/update videos")
    for video in new_videos:
        # id video
        id_video = str(video["id_video"]).strip()

        # add the video to the db if needed
        if id_video not in old_videos:
            # add thumbnail details
            video = enhance_video(video)
            # add to db
            try:
                with Session(engine) as session:
                    session.add(Videos(**video))
                    session.commit()
                    added += 1
            except Exception as e:
                logging.error("add video")
                logging.error(e)
                logging.error(video)
                errors_added += 1
        # else update the video
        else:
            # do not update each time
            if not random.randint(0, 3):
                continue
            # update the video
            try:
                with Session(engine) as session:
                    session.query(Videos).filter_by(id_video=id_video).update(video)
                    session.commit()
                    updated += 1
            except Exception as e:
                logging.error("update video")
                logging.error(e)
                logging.error(video)
                errors_updated += 1

    time_add_update_videos = round(time.time() - t0, 4)

    payload = {
        "ok": {
            "added": added,
            "updated": updated,
        },
        "errors": {
            "errors_added": errors_added,
            "errors_updated": errors_updated,
        },
        "counts": {
            "old_videos_count": old_videos_count,
            "new_videos_count": new_videos_count,
        },
        "timers": {
            "time_load_channels": time_load_channels,
            "time_get_feeds": time_get_feeds,
            "time_load_videos": time_load_videos,
            "time_add_update_videos": time_add_update_videos,
            "time_total": round(time.time() - T0, 4),
        },
    }

    return jsonify(payload, message="Done")


if __name__ == "__main__":
    from src.params import get_params
    from src.models.db import Db

    from fastapi import FastAPI, HTTPException, APIRouter, Depends
    from src.models import *
    from src.routers.helpers import jsonify
    from src.queries import query_all, VideoQuery
    from src.models.db import Channels, Videos, session, engine, Session
    from src.core.feeds import extract_rss
    import logging
    import time
    import pandas as pd

    from src.core.thumbnails import enhance_video
    from src.routers.helpers import jsonify, validate_token  # token_required
    import random

    params = get_params(MODE="dev")
    engine = Db.engine(params=params)
