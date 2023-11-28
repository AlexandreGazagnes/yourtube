import logging

from fastapi import FastAPI, HTTPException, APIRouter

from src.helpers.queries import query_all
from src.helpers.routers import jsonify

from src.channels.models import Channel
from src.channels.validators import ChannelValidator
from src.channels.helpers import ChannelHelper


channels = APIRouter(
    prefix="/channels",
    tags=["channels"],
)


@channels.post("", status_code=201)
async def add_channel(
    channel: ChannelValidator.base = ChannelValidator.default,
):
    """Add a channel"""

    if response := ChannelHelper.default(channel):
        raise response

    if response := ChannelHelper.no_channel_id(channel):
        raise response

    if response := ChannelHelper.already_in_db(channel):
        raise response

    if response := ChannelHelper.create_channel(channel):
        raise response

    return jsonify(channel, message="Channel added")


@channels.put("/{id_channel}", status_code=201)
async def update_channel(id_channel: str, channel: ChannelValidator.base):
    """Update a channel"""

    raise HTTPException(status_code=501, detail="Not implemented")


@channels.get("/", status_code=200)
async def get_all_channels():
    """Get all channels"""

    payload = query_all(Channel)
    return jsonify(payload=payload, message="done")


@channels.get("/by_user/{id_user}", status_code=200)
async def get_all_channels(id_user: int):
    """Get all channels by user"""

    payload = query_all(Channel)
    return jsonify(payload=payload, message="done")
