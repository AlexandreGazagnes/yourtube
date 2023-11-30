import logging

from fastapi import FastAPI, HTTPException, APIRouter
from src.videos.models import *
from src.videos.queries import VideoQuery
from src.videos.validators import VideoValidator

from src.helpers.routers import jsonify
from src.db import Session, engine

# from src.validators import ChannelBase, default_channel


videos = APIRouter(
    prefix="/videos",
    tags=["videos"],
)


@videos.get("")
async def get_all_videos(
    query: str | None = None,
    limit: int = 200,
    last_days: int = 4,
    duration_min: int = 3 * 60,
    duration_max: int = 10 * 3600,
    # categ_1: list = None,
    # language: list = None,
    # status: list = None,
    # watched: int = -1,
    order_by: str = "published",
):
    """Get all videos"""

    # if query overide params
    if query:
        last_days = 10_000
        limit = 10_000

    payload = VideoQuery.all(
        query=query,
        limit=limit,
        last_days=last_days,
        duration_min=duration_min,
        duration_max=duration_max,
        order_by=order_by,
    )
    return jsonify(payload)


@videos.get("/{id_video}", status_code=200)
async def get_a_video(id_video: str):
    """Get a video"""

    raise HTTPException(status_code=501, detail="Not implemented")


@videos.put("/{id_video}", status_code=201)
async def update_a_video(id_video: str, video: VideoValidator.base):
    """Update a video"""

    raise HTTPException(status_code=501, detail="Not implemented")


@videos.get("/by_user/{id_user}")
async def get_videos_by_user(
    id_user: int,
    query: str | None = None,
    limit: int = 200,
    last_days: int = 4,
    duration_min: int = 3 * 60,
    duration_max: int = 10 * 3600,
    # categ_1: list = None,
    # language: list = None,
    # status: list = None,
    # watched: int = -1,
    order_by: str = "published",
):
    """Get all videos by user"""

    if query:
        last_days = 10_000
        limit = 10_000

    payload = VideoQuery.by_user(
        id_user=id_user,
        query=query,
        limit=limit,
        last_days=last_days,
        duration_min=duration_min,
        duration_max=duration_max,
        order_by=order_by,
    )

    return jsonify(payload)


# @videos.get("/by_categ_1")
# async def get_videos_by_category(
#     limit: int = 100,
#     last_days: int = 2,
# ):
#     """Get all videos by category 1"""

#     pass


# @videos.get("/by_categ_2")
# async def get_videos_by_category(
#     limit: int = 100,
#     last_days: int = 2,
# ):
#     """Get all videos by category 2"""

#     pass


# @videos.get("/by_language")
# async def get_videos_by_language(
#     limit: int = 100,
#     last_days: int = 2,
# ):
#     """Get all videos by language"""

#     pass


# @videos.get("/by_status")
# async def get_videos_by_status(
#     limit: int = 100,
#     last_days: int = 2,
# ):
#     """Get all videos by status"""

#     pass


# @videos.get("/by_watched")
# async def get_videos_by_watched(
#     limit: int = 100,
#     last_days: int = 2,
# ):
#     """Get all videos by watched"""

#     pass


# @videos.get("/by_channel")
# async def get_videos_by_channel(
#     limit: int = 100,
#     last_days: int = 2,
# ):
#     """Get all videos by channel"""

#     pass
