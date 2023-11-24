from fastapi import FastAPI, HTTPException, APIRouter
from src.models import *
from src.routers.helpers import jsonify
from src.queries import query_all, VideoQuery
from src.models.db import Channels, Videos, session, engine, Session
from src.core.feeds import extract_rss
import logging

# from src.queries import query_all, jsonify

# from src.validators import ChannelBase, default_channel

import logging


home = APIRouter(
    prefix="",
    tags=["home"],
)


@home.get("/", status_code=200)
async def root():
    return jsonify(None, message="Hello World")


@home.get("/update", status_code=200)
async def update():
    """ """

    # load channels
    channel_list = [i.get("id_channel") for i in query_all(Channels, limit=1_000)]

    # feeds
    feeds = [extract_rss(i) for i in channel_list]
    new_videos = []
    _ = [new_videos.extend(i) for i in feeds]

    # load videos
    old_videos = [
        i.get("id_video") for i in VideoQuery.all(limit=5_000, last_days=1_000)
    ]

    for video in new_videos:
        # manage the id video
        if "id_video" not in video.keys():
            id_video = video.get("yt_videoid")
            video["id_video"] = id_video

        # clean the video dict
        video = {i: j for i, j in video.items() if i in Videos.__table__.columns.keys()}

        # add the video to the db if needed
        if video["id_video"] not in old_videos:
            try:
                with Session(engine) as session:
                    session.add(Videos(**video))
                    session.commit()
            except Exception as e:
                logging.error(e)
                logging.error(video)
        # else update the video
        else:
            try:
                with Session(engine) as session:
                    session.query(Videos).filter_by(id_video=video["id_video"]).update(
                        video
                    )
                    session.commit()
            except Exception as e:
                logging.error(e)
                logging.error(video)

    # #     return jsonify(None, message="Done")
