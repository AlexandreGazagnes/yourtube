import logging

from fastapi import FastAPI, HTTPException, APIRouter

# from src.helpers.queries import ChannelQuery
from src.helpers.routers import jsonify

from src.channels.models import Channel

# from src.channels.validators import ChannelValidator
# from src.channels.helpers import ChannelHelper
from src.channels.queries import ChannelQuery, ChannelsQueries


#############################
# CHANNEL
#############################

channel = APIRouter(
    prefix="/channel",
    tags=["channel"],
)


@channel.get("", status_code=200)
async def get_channel(id_channel: str):
    """Get a channel"""

    results = ChannelQuery.by_id_channel(id_channel)

    return {
        "channel": results,
        "message": "done",
        "total": 1,
        "limit": 1,
        "skip": 0,
    }


#############################
# CHANNELS
#############################


channels = APIRouter(
    prefix="/channels",
    tags=["channels"],
)


@channels.get("", status_code=200)
async def get_all_channels(
    limit: int = -1,
    skip: int = 0,
    order_by: str | None = None,
    order_direction: str = "desc",
):
    """Get all channels"""

    results, total = ChannelsQueries.all(
        limit=limit,
        skip=skip,
        order_by=order_by,
        order_direction=order_direction,
    )

    return {
        "channels": results,
        "total": total,
        "skip": skip,
        "limit": limit,
        "message": "done",
    }


# @channel.post("", status_code=201)
# async def add_channel(
#     channel: ChannelValidator.base = ChannelValidator.default,
# ):
#     """Add a channel"""

#     if response := ChannelHelper.default(channel):
#         raise response

#     if response := ChannelHelper.no_channel_id(channel):
#         raise response

#     if response := ChannelHelper.already_in_db(channel):
#         raise response

#     if response := ChannelHelper.create_channel(channel):
#         raise response

#     return jsonify(channel, message="Channel added")


# @channel.put("/{id_channel}", status_code=201)
# async def update_channel(id_channel: str, channel: ChannelValidator.base):
#     """Update a channel"""

#     raise HTTPException(status_code=501, detail="Not implemented")


@channels.get("/by_user", status_code=200)
async def get_channels_by_user(
    id_user: int,
    limit: int = -1,
    skip: int = 0,
    order_by: str = "id_channel",
    order_direction: str = "desc",
):
    """Get all channels by user"""

    # not implemented

    results, total = ChannelsQueries.by_user(
        id_user,
        limit=limit,
        skip=skip,
        order_by=order_by,
        order_direction=order_direction,
    )

    return {
        "channels": results,
        "total": total,
        "skip": skip,
        "limit": limit,
        "message": "done",
    }

    # payload = query_all(Channel)
    # return jsonify(payload=payload, message="done")
    # raise HTTPException(status_code=501, detail="Not implemented")


@channels.get("/by_categ_1", status_code=200)
async def get_channels_by_categ_1(
    id_user: int,
    id_categ_1: str,
    limit: int = -1,
    skip: int = 0,
    order_by: str | None = None,
    order_direction: str = "desc",
):
    """Get all channels by user"""

    # not implemented

    results, total = ChannelsQueries.by_categ_1(
        id_user,
        id_categ_1,
        limit=limit,
        skip=skip,
        order_by=order_by,
        order_direction=order_direction,
    )

    return {
        "channels": results,
        "total": total,
        "skip": skip,
        "limit": limit,
        "message": "done",
    }
