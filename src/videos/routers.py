import logging

from fastapi import FastAPI, HTTPException, APIRouter
from src.videos.models import *
from src.videos.queries import VideoQuery
from src.videos.validators import VideoValidator

from src.helpers.routers import jsonify
from src.db import Session, engine


# from src.validators import ChannelBase, default_channel

import logging


videos = APIRouter(
    prefix="/videos",
    tags=["videos"],
)


@videos.get("")
async def get_all_videos(
    limit: int = 100,
    last_days: int = 4,
):
    """Get all videos"""

    payload = VideoQuery.all(limit=limit, last_days=last_days)
    return jsonify(payload)


@videos.put("/{id_video}", status_code=201)
async def update_videos(id_video: str, video: VideoValidator.base):
    """Update a video"""

    raise HTTPException(status_code=501, detail="Not implemented")


@videos.get("/by_categ_1")
async def get_videos_by_category(
    limit: int = 100,
    last_days: int = 2,
):
    """Get all videos by category 1"""

    pass


@videos.get("/by_categ_2")
async def get_videos_by_category(
    limit: int = 100,
    last_days: int = 2,
):
    """Get all videos by category 2"""

    pass


@videos.get("/by_language")
async def get_videos_by_language(
    limit: int = 100,
    last_days: int = 2,
):
    """Get all videos by language"""

    pass


@videos.get("/by_status")
async def get_videos_by_status(
    limit: int = 100,
    last_days: int = 2,
):
    """Get all videos by status"""

    pass


@videos.get("/by_watched")
async def get_videos_by_watched(
    limit: int = 100,
    last_days: int = 2,
):
    """Get all videos by watched"""

    pass


@videos.get("/by_channel")
async def get_videos_by_channel(
    limit: int = 100,
    last_days: int = 2,
):
    """Get all videos by channel"""

    pass
