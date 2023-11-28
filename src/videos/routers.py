from typing import List, Optional, Union
from fastapi import FastAPI, HTTPException, APIRouter
from src.models.db import *
from src.queries import VideoQuery
from src.routers.helpers import jsonify
from src.validators import VideoValidator

# from src.validators import ChannelBase, default_channel

import logging


videos = APIRouter(
    prefix="/videos",
    tags=["videos"],
)


@videos.get("")
async def get_all_videos(
    limit: int = 100,
    last_days: int = 2,
):
    payload = VideoQuery.all(limit=limit, last_days=last_days)
    return jsonify(payload)


@videos.put("/{id_video}", status_code=201)
async def update_videos(id_video: str, video: VideoValidator.base):
    raise HTTPException(status_code=501, detail="Not implemented")


@videos.get("/by_categ_1")
async def get_videos_by_category(
    limit: int = 100,
    last_days: int = 1,
):
    pass


@videos.get("/by_categ_2")
async def get_videos_by_category(
    limit: int = 100,
    last_days: int = 1,
):
    pass


@videos.get("/by_language")
async def get_videos_by_language(
    limit: int = 100,
    last_days: int = 1,
):
    pass


@videos.get("/by_status")
async def get_videos_by_status(
    limit: int = 100,
    last_days: int = 1,
):
    pass


@videos.get("/by_watched")
async def get_videos_by_watched(
    limit: int = 100,
    last_days: int = 1,
):
    pass


@videos.get("/by_channel")
async def get_videos_by_channel(
    limit: int = 100,
    last_days: int = 1,
):
    pass
