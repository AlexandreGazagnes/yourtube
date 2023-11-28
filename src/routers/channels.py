from fastapi import FastAPI, HTTPException, APIRouter
from src.models.db import *
from src.queries import query_all
from src.routers.helpers import jsonify

from src.validators import ChannelValidator

import logging


channels = APIRouter(
    prefix="/channels",
    tags=["channels"],
)


@channels.post("", status_code=201)
async def add_channel(
    channel: ChannelValidator.base = ChannelValidator.default,
):
    """ """

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
    """ """

    raise HTTPException(status_code=501, detail="Not implemented")


@channels.get("/", status_code=200)
async def get_all_channels():
    return jsonify(query_all(Channels))


@channels.get("/by_user/{id_user}", status_code=200)
async def get_all_channels(id_user: int):
    return jsonify(query_all(Channels))
