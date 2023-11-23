from fastapi import FastAPI, HTTPException, APIRouter
from src.models.db import *
from src.queries import query_all
from src.validators import Validators

import logging


channels = APIRouter(
    prefix="/channels",
    tags=["channels"],
)


@channels.post("", status_code=201)
async def add_channel(
    channel: Validators.channels.base = Validators.channels.default,
):
    """ """

    if channel == Validators.channels.default:
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
        return {"message": "Channel added"}


@channels.put("", status_code=201)
async def update_channel(channel):
    """ """

    raise HTTPException(status_code=501, detail="Not implemented")


@channels.get("/", status_code=200)
async def get_all_channels():
    return query_all(Channels)
