import logging

from fastapi import FastAPI, HTTPException, APIRouter

# from src.helpers.queries import ChannelQuery
from src.helpers.routers import jsonify

from src.channels.models import Channel

# from src.channels.validators import ChannelValidator
# from src.channels.helpers import ChannelHelper
from src.channels.queries import ChannelQuery, ChannelsQueries


channel = APIRouter(
    prefix="/channel",
    tags=["channel"],
)


#############################
# CHANNEL
#############################


@channel.get("/{id_channel}", status_code=200)
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


channels = APIRouter(
    prefix="/channels",
    tags=["channels"],
)


#############################
# CHANNELS
#############################


@channels.get("", status_code=200)
async def get_all_channels():
    """Get all channels"""

    results = ChannelQuery.all(Channel)
    total = len(results)
    skip = 0
    limit = total

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
async def get_channels_by_suer(
    id_user: int,
    limit: int | None = None,
    skip: int | None = None,
    order_by: str = "id_channel",
    order_direction: str = "desc",
):
    """Get all channels by user"""

    # not implemented

    results = ChannelQuery.by_user(
        id_user,
        limit=limit,
        skip=skip,
        order_by=order_by,
        order_direction=order_direction,
    )

    return {
        "channels": results,
        "total": len(results),
        "skip": skip,
        "limit": limit,
        "message": "done",
    }

    # payload = query_all(Channel)
    # return jsonify(payload=payload, message="done")
    # raise HTTPException(status_code=501, detail="Not implemented")
