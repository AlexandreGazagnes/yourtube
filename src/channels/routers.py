import logging

from fastapi import FastAPI, HTTPException, APIRouter

from src.helpers.queries import query_all
from src.helpers.routers import jsonify

from src.channels.models import Channels
from src.channels.validators import ChannelValidator


channels = APIRouter(
    prefix="/channels",
    tags=["channels"],
)


@channels.post("", status_code=201)
async def add_channel(
    channel: ChannelValidator.base = ChannelValidator.default,
):
    """Add a channel"""

    if channel == ChannelValidator.default:
        logging.warning("Using default channel")

        # return {"message": "Using default channel no db changes"}
        raise HTTPException(
            status_code=204, detail="Using default channel no db changes"
        )

    if not channel.id_channel:
        logging.error("id_channel is required")
        # TODO ADD GATHER THE TRUE ID CHANNEL
        pass

    with Session(engine) as session:
        channel = Channels(**channel.model_dump())
        session.add(channel)
        session.commit()
        return jsonify(None, message="Channel added")


@channels.put("/{id_channel}", status_code=201)
async def update_channel(id_channel: str, channel: ChannelValidator.base):
    """Update a channel"""

    raise HTTPException(status_code=501, detail="Not implemented")


@channels.get("/", status_code=200)
async def get_all_channels():
    """Get all channels"""
    return jsonify(query_all(Channels))


@channels.get("/by_user/{id_user}", status_code=200)
async def get_all_channels(id_user: int):
    """Get all channels by user"""

    return jsonify(query_all(Channels))
