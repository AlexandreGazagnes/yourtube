import logging

from fastapi import FastAPI, HTTPException, APIRouter
from src.videos.models import *
from src.videos.queries import VideoQuery, VideosQueries
from src.videos.validators import VideoValidator

from src.helpers.routers import jsonify
from src.db import Session, engine

from src.videos.validators import VideoValidator

# from src.validators import ChannelBase, default_channel


############################
#   VIDEO
#############################

video = APIRouter(
    prefix="/video",
    tags=["video"],
)


@video.get("/{id_video}", status_code=200)
async def get_a_video(id_video: str):
    """Get a video"""

    results = VideoQuery.by_id_video(id_video)

    return {
        "video": results,
        "message": "done",
        "total": 1,
        "limit": 1,
        "skip": 0,
    }


# @video.post("/{id_video}", status_code=201)
# async def update_a_video_watched(id_video: str):
#     """Update a video watched"""

#     raise HTTPException(status_code=501, detail="Not implemented")


# @video.put("/{id_video}", status_code=201)
# async def update_a_video(id_video: str, video: VideoValidator.base):
#     """Update a video"""

#     raise HTTPException(status_code=501, detail="Not implemented")


# @video.delete("/{id_video}", status_code=201)
# async def delete_a_video(id_video: str):
#     """Delete a video"""

#     raise HTTPException(status_code=501, detail="Not implemented")


############################
#   VIDEOS
#############################

videos = APIRouter(
    prefix="/videos",
    tags=["videos"],
)


@videos.get("")
async def get_all_videos(
    query: str | None = None,
    skip: int = 0,
    limit: int = 200,
    days_min: int = 0,
    days_max: int = 30,
    duration_min: int = 3 * 60,
    duration_max: int = 10 * 3600,
    id_language: str | None = None,
    watched: int = -1,
    order_by: str = "published",
    order_direction: str = "desc",
    id_categ_0: str | None = None,
    id_categ_1: str | None = None,
    id_categ_2: str | None = None,
    id_status: str | None = None,
):
    """Get all videos"""

    video_list, total = VideosQueries.all(
        query,
        skip,
        limit,
        days_min,
        days_max,
        duration_min,
        duration_max,
        id_language,
        watched,
        order_by,
        order_direction,
        id_categ_0,
        id_categ_1,
        id_categ_2,
        id_status,
    )

    return {
        "videos": video_list,
        "total": total,
        "skip": skip,
        "limit": limit,
        "message": "done",
        "params": {},
    }


@videos.get("/by_user", status_code=200)
async def get_videos_by_user(
    id_user: int | None,
    query: str | None = None,
    skip: int = 0,
    limit: int = 200,
    days_min: int = 0,
    days_max: int = 30,
    duration_min: int = 3 * 60,
    duration_max: int = 10 * 3600,
    id_language: str | None = None,
    watched: int = -1,
    order_by: str = "published",
    order_direction: str = "desc",
    id_categ_0: str | None = None,
    id_categ_1: str | None = None,
    id_categ_2: str | None = None,
    id_status: str | None = None,
):
    """Get all videos"""

    video_list, total = VideosQueries.by_user(
        id_user,
        query,
        skip,
        limit,
        days_min,
        days_max,
        duration_min,
        duration_max,
        id_language,
        watched,
        order_by,
        order_direction,
        id_categ_0,
        id_categ_1,
        id_categ_2,
        id_status,
    )

    return {
        "videos": video_list,
        "total": total,
        "skip": skip,
        "limit": limit,
        "message": "done",
        "params": {},
    }


@videos.get("/by_channel", status_code=200)
async def get_videos_by_channel(
    id_channel: str | None,
    query: str | None = None,
    skip: int = 0,
    limit: int = 200,
    days_min: int = 0,
    days_max: int = 30,
    duration_min: int = 3 * 60,
    duration_max: int = 10 * 3600,
    id_language: str | None = None,
    watched: int = -1,
    order_by: str = "published",
    order_direction: str = "desc",
    id_categ_0: str | None = None,
    id_categ_1: str | None = None,
    id_categ_2: str | None = None,
    id_status: str | None = None,
):
    """Get all videos"""

    video_list, total = VideosQueries.by_channel(
        id_channel,
        query,
        skip,
        limit,
        days_min,
        days_max,
        duration_min,
        duration_max,
        id_language,
        watched,
        order_by,
        order_direction,
        id_categ_0,
        id_categ_1,
        id_categ_2,
        id_status,
    )

    return {
        "videos": video_list,
        "total": total,
        "skip": skip,
        "limit": limit,
        "message": "done",
        "params": {},
    }


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
