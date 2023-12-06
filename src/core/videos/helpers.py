"""
Helper module 
submodule of core/videos/functions with helpers (sub functions)
laod channels, videos, clean videos, add/update videos to db
scrap feeds, update feeds, reshape payload etc etc
"""


import os, sys, logging, time, random

from src.db import Session, engine

from src.videos.models import Video
from src.videos.models import DEFAULT_DURATION, DEFAULT_THUMBNAIL_VIDEO_URL
from src.videos.queries import VideoQuery

from src.channels.models import Channel
from src.channels.queries import ChannelQuery

from src.helpers.queries import query_all
from src.helpers.helpers import make_now

from src.core.videos.rss import CoreVideoRss


def _clean_video_list(video_list: list[dict]) -> list[dict]:
    """be sure that no useless keys are in the video dict and id_video ok"""

    for i, video in enumerate(video_list):
        # manage the id video
        if "id_video" not in video.keys():
            video_list[i]["id_video"] = video.get("yt_videoid")

        # clean the video dict
        video_list[i] = {
            i: j
            for i, j in video_list[i].items()
            if i in Video.__table__.columns.keys()
        }

    return video_list


def _scrap_feeds(
    channel_list_ids: list[str],
    scrap: bool = True,
    detail: bool = True,
    clean: bool = True,
    parallel: bool = True,
) -> tuple[list[dict], float]:
    """scrap feeds form list of channel id and add detail and clean"""

    # timer
    t0 = time.time()

    logging.info("get feeds")

    # do scrap
    if scrap:
        new_videos = CoreVideoRss.scrap_list(channel_list_ids, parallel=parallel)

    # add detail
    if detail:
        new_videos = CoreVideoRss.update_list(
            new_videos, detail=True, parallel=parallel
        )

    # clean
    if clean:
        new_videos = _clean_video_list(new_videos)

    # timer
    time_get_feeds = round(time.time() - t0, 4)

    return new_videos, time_get_feeds


def _update_feeds(
    feeds_list: list[dict],
    detail: bool = True,
    categ_1: bool = True,
    clean: bool = True,
    parallel: bool = True,
) -> tuple[list[dict], float]:
    """from feed list add detail and categ and clean"""

    # timer
    t0 = time.time()

    logging.warning("get feeds")

    # video detail
    if detail:
        feeds_list = CoreVideoRss.update_list(
            feeds_list,
            detail=True,
            parallel=parallel,
        )

    # categ 1
    if categ_1:
        feeds_list = CoreVideoRss.update_list(
            feeds_list,
            categ_1=True,
            detail=False,
            parallel=parallel,
        )

    # clean
    if clean:
        feeds_list = _clean_video_list(feeds_list)

    # timer
    time_get_feeds = round(time.time() - t0, 4)

    return feeds_list, time_get_feeds


def _make_payload() -> dict:
    """build placeholder payload"""

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
    new: bool = True,
    old: bool = True,
    enhance_old: bool = False,
    random_: bool = True,
    engine=engine,
) -> dict:
    """add/update videos to db"""

    # timer
    t0 = time.time()

    logging.info("add/update videos")

    for video in new_videos:
        id_video = str(video["id_video"]).strip()  # id video

        if (
            id_video not in old_videos_ids
        ) and new:  # add the video to the db if needed
            try:
                with Session(engine) as session:
                    session.add(Video(**video))
                    session.commit()
                    payload["added"] += 1
            except Exception as e:
                logging.error(f"{e} - add video -> {video}")
                payload["errors_added"] += 1

        else:  # update the video
            if not old:  # if old is False, do not update
                continue

            # randomize the update if needed
            if not random_:
                if not random.randint(0, 3):  # do not update each time
                    continue

            # enhance video
            if enhance_old:  # enhance video
                try:
                    video = CoreVideoRss.update_one(video, detail=True, categ_1=True)
                except Exception as e:
                    logging.error(f"{e} - enhance video -> {video}")

            # do update
            try:
                with Session(engine) as session:
                    video["updated_at"] = make_now()
                    session.query(Video).filter_by(id_video=id_video).update(video)
                    session.commit()
                    payload["updated"] += 1
            except Exception as e:
                logging.error(f"update video - {e} - {video}")
                payload["errors_updated"] += 1

    # timer
    payload["time_add_update_videos"] = round(time.time() - t0, 4)

    return payload


def _reshape_payload(payload: dict, T0: float) -> dict:
    """reshape payload before sending"""

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


def _get_broken_videos(
    shuffle_: bool = True,
    clean: bool = True,
) -> list[dict]:
    """return list of videos if broken (ie respond criterions such as category, duration etc)"""

    # query all videos
    broken_videos = VideoQuery.all(clean_duration_=False)

    # filter function
    f = (
        lambda i: (i["category"] == "Unknown")
        or (i["id_categ_1"] == "?")
        or (i["duration"] == DEFAULT_DURATION)
        or (i["thumbnail_video_url"] == DEFAULT_THUMBNAIL_VIDEO_URL)
    )

    # perform filter
    broken_videos = [i for i in broken_videos if f(i)]

    # shuffle if needed
    if shuffle_:
        random.shuffle(broken_videos)

    # clean if needed
    if clean:
        broken_videos = _clean_video_list(broken_videos)

    return broken_videos


class CoreVideoHelpers:
    """Helper class for core videos functions
    public methods:
        - scrap_feeds
        - update_feeds
        - make_payload
        - reshape_payload
        - add_update_db
        - get_broken_videos
    """

    scrap_feeds = _scrap_feeds
    update_feeds = _update_feeds
    make_payload = _make_payload
    reshape_payload = _reshape_payload
    add_update_db = _add_update_db
    get_broken_videos = _get_broken_videos
