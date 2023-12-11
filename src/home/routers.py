import logging, time, random

from fastapi import FastAPI, HTTPException, APIRouter, Depends

from src.db import Channel, Video, session, engine, Session
from src.helpers.routers import jsonify, validate_token  # token_required
from src.helpers.queries import query_all

# from src.home.helpers import HomeHelpers
# from src.home.functions import HomeFunctions
from src.videos.queries import VideosQueries

# from src.queries import query_all, jsonify
# from src.validators import ChannelBase, default_channel
# import pandas as pd

# from src.videos.models import Video
# logging.basicConfig(level=logging.INFO)

home = APIRouter(
    prefix="",
    tags=["home"],
)


@home.get("/", status_code=200)
async def root():
    """say hello"""

    return jsonify("", message="Hello World")


@home.get("/ping", status_code=200)
async def ping():
    """ping the app"""

    return jsonify("", message="pong")


@home.get("/state", status_code=200)
async def state():
    """Get the state of the app"""

    result = VideosQueries.count()
    return jsonify({"video_count": result}, message="success")


# @home.get("/update", status_code=200)
# async def update(token: str = Depends(validate_token)):
#     """Update bdd with new feeds"""

#     payload = HomeFunctions.update()

#     return jsonify(payload, message="Done")


# if __name__ == "__main__":
#     from src.params import get_params
#     from src.models.db import Db

#     from fastapi import FastAPI, HTTPException, APIRouter, Depends
#     from src.models import *
#     from src.routers.helpers import jsonify
#     from src.queries import query_all, VideoQuery
#     from src.models.db import Channels, Videos, session, engine, Session
#     from src.core.feeds import extract_rss
#     import logging
#     import time
#     import pandas as pd

#     from src.core.thumbnails import enhance_video
#     from src.routers.helpers import jsonify, validate_token  # token_required
#     import random

#     params = get_params(MODE="dev")
#     engine = Db.engine(params=params)
