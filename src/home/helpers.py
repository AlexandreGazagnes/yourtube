import os, sys, logging, time, random
from src.db import Session, engine

from src.videos.models import Video
from src.videos.queries import VideoQuery

from src.channels.models import Channel
from src.core.thumbnails import enhance_video
from src.helpers.queries import query_all

from src.channels.queries import ChannelQuery
from src.core.feeds import extract_rss, extract_rss_and_flatten
from src.core.thumbnails import enhance_video


def _load_channels_ids():
    """ """

    t0 = time.time()

    logging.warning("load channels")

    # with Session(engine) as session:
    # channel_list_ids = [
    #     i.get("id_channel") for i in query_all(Channel, limit=10_000)
    # ]
    channel_list_ids = ChannelQuery.all_id_channel()
    channel_list_ids = [i for i in channel_list_ids if not i.lower().startswith("fake")]
    channel_list_ids = [i for i in channel_list_ids if not i.lower().startswith("test")]

    time_load_channels = round(time.time() - t0, 4)

    return channel_list_ids, time_load_channels


def _load_old_videos_ids():
    """ """

    t0 = time.time()

    logging.warning("load videos")

    # with Session(engine) as session:
    old_videos_ids = VideoQuery.all_id_videos()

    time_load_videos = round(time.time() - t0, 4)

    return old_videos_ids, time_load_videos


def _load_feeds(channel_list_ids):
    """ """

    t0 = time.time()

    logging.warning("get feeds")

    new_videos = extract_rss_and_flatten(channel_list_ids)

    time_get_feeds = round(time.time() - t0, 4)

    return new_videos, time_get_feeds


def _clean_new_videos(new_videos):
    """ """

    for i, video in enumerate(new_videos):
        # manage the id video

        if "id_video" not in video.keys():
            new_videos[i]["id_video"] = video.get("yt_videoid")

        # clean the video dict
        new_videos[i] = {
            i: j
            for i, j in new_videos[i].items()
            if i in Video.__table__.columns.keys()
        }

    return new_videos


def _make_payload():
    payload = {
        "added": 0,
        "updated": 0,
        "errors_added": 0,
        "errors_updated": 0,
    }
    return payload


def _add_update_db(
    new_videos: list,
    old_videos_ids: list,
    payload: dict,
) -> dict:
    """add/update videos to db"""

    t0 = time.time()
    logging.warning("add/update videos")

    for video in new_videos:
        id_video = str(video["id_video"]).strip()  # id video

        if id_video not in old_videos_ids:  # add the video to the db if needed
            video = enhance_video(video)  # enhance

            try:
                with Session(engine) as session:
                    session.add(Video(**video))
                    session.commit()
                    payload["added"] += 1
            except Exception as e:
                logging.error(f"{e} - add video -> {video}")
                payload["errors_added"] += 1

        else:  # update the video
            if not random.randint(0, 3):  # do not update each time
                continue
            try:
                with Session(engine) as session:
                    session.query(Video).filter_by(id_video=id_video).update(video)
                    session.commit()
                    payload["updated"] += 1
            except Exception as e:
                logging.error(f"update video - {e} - {video}")
                payload["errors_updated"] += 1

    payload["time_add_update_videos"] = round(time.time() - t0, 4)

    return payload


def _reshape_payload(payload, T0):
    """reshape payload"""

    payload = {
        "ok": {
            "added": payload["added"],
            "updated": payload["updated"],
        },
        "errors": {
            "errors_added": payload["errors_added"],
            "errors_updated": payload["errors_updated"],
        },
        "counts": {
            "old_videos_count": payload["old_videos_count"],
            "new_videos_count": payload["new_videos_count"],
        },
        "timers": {
            "time_load_channels": payload["time_load_channels"],
            "time_get_feeds": payload["time_get_feeds"],
            "time_load_videos": payload["time_load_videos"],
            "time_add_update_videos": payload["time_add_update_videos"],
            "time_total": round(time.time() - T0, 4),
        },
    }

    return payload


class HomeHelpers:
    """Home Helpers"""

    load_channels_ids = _load_channels_ids
    load_feeds = _load_feeds
    clean_new_videos = _clean_new_videos
    load_old_videos_ids = _load_old_videos_ids
    make_payload = _make_payload
    add_update_db = _add_update_db
    reshape_payload = _reshape_payload
