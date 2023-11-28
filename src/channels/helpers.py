import logging

from fastapi import HTTPException

from src.channels.validators import ChannelValidator
from src.channels.queries import ChannelQuery
from src.channels.models import Channels

from src.helpers.routers import jsonify

from src.db import Session, engine


def _manage_default(channel: ChannelValidator.base):
    """Manage default channel"""

    if channel.id_channel == ChannelValidator.default.id_channel:
        logging.warning(f"Channel {channel.id_channel} is default")
        return HTTPException(
            status_code=409,
            detail=f"Channel {channel.id_channel} is default",
        )


def _manage_no_channel_id(channel: ChannelValidator.base):
    """Manage no channel id"""

    if not channel.id_channel:
        logging.error("id_channel is required")
        return HTTPException(
            status_code=400,
            detail="id_channel is required",
        )


def _manage_already_in_db(channel: ChannelValidator.base):
    """Check if channel already exists"""

    if channel.id_channel in ChannelQuery.all_id_channel():
        return HTTPException(
            status_code=409,
            detail=f"Channel {channel.id_channel} for channel {channel} already exists",
        )


def _create_channel(channel: ChannelValidator.base):
    """Create a channel"""

    try:
        with Session(engine) as session:
            channel = Channels(**channel.model_dump())
            session.add(channel)
            session.commit()

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error : {e}")


class ChannelHelper:
    default = _manage_default
    no_channel_id = _manage_no_channel_id
    already_in_db = _manage_already_in_db
    create_channel = _create_channel
