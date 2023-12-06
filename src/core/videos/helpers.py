import os, sys, logging, time, random
from src.db import Session, engine

from src.videos.models import Video
from src.videos.queries import VideoQuery

from src.channels.models import Channel
from src.core.videos.DEPRECATED_rapid_api import enhance_video
from src.helpers.queries import query_all

from src.channels.queries import ChannelQuery

# from src.core.feeds import extract_rss, extract_rss_and_flatten
from src.core.videos.DEPRECATED_rapid_api import enhance_video
from src.helpers.helpers import make_now
from src.core.videos.rss import _scrap_rss_list, _update_rss_list, _update_one_rss


from src.videos.models import DEFAULT_DURATION, DEFAULT_THUMBNAIL_VIDEO_URL


def load_channels_ids() -> tuple[list[str], float]:
    """ """

    t0 = time.time()

    logging.warning("load channels")

    channel_list_ids = ChannelQuery.all_id_channel()
    channel_list_ids = [i for i in channel_list_ids if not i.lower().startswith("fake")]
    channel_list_ids = [i for i in channel_list_ids if not i.lower().startswith("test")]

    time_load_channels = round(time.time() - t0, 4)

    return channel_list_ids, time_load_channels


def load_old_videos_ids() -> tuple[list[str], float]:
    """ """

    t0 = time.time()
    logging.warning("load videos")

    old_videos_ids = VideoQuery.all_id_videos()
    time_load_videos = round(time.time() - t0, 4)

    return old_videos_ids, time_load_videos


def clean_video_list(video_list: list[dict]) -> list[dict]:
    """ """

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


def scrap_feeds(
    channel_list_ids: list[str],
    scrap: bool = True,
    detail: bool = True,
    clean: bool = True,
    parallel: bool = True,
) -> tuple[list[dict], float]:
    """scrap feeds form list of channel id and add detail and clean"""

    t0 = time.time()

    logging.warning("get feeds")
    if scrap:
        new_videos = _scrap_rss_list(channel_list_ids, parallel=parallel)

    if detail:
        new_videos = _update_rss_list(new_videos, detail=True, parallel=parallel)

    if clean:
        new_videos = clean_video_list(new_videos)

    time_get_feeds = round(time.time() - t0, 4)

    return new_videos, time_get_feeds


def update_feeds(
    feeds_list: list[dict],
    video_detail: bool = True,
    categ_1: bool = True,
    clean: bool = True,
    parallel: bool = True,
) -> tuple[list[dict], float]:
    """from feed list add detail and categ and clean"""

    t0 = time.time()

    logging.warning("get feeds")

    if video_detail:
        feeds_list = _update_rss_list(
            feeds_list,
            detail=True,
            parallel=parallel,
        )

    if categ_1:
        feeds_list = _update_rss_list(
            feeds_list,
            categ_1=True,
            detail=False,
            parallel=parallel,
        )

    if clean:
        feeds_list = clean_video_list(feeds_list)

    time_get_feeds = round(time.time() - t0, 4)

    return feeds_list, time_get_feeds


def make_payload() -> dict:
    payload = {
        "added": 0,
        "updated": 0,
        "errors_added": 0,
        "errors_updated": 0,
    }
    return payload


def add_update_db(
    new_videos: list,
    old_videos_ids: list,
    payload: dict,
    new=True,
    old=True,
    # enhance_new=True,
    enhance_old=False,
    random_=True,
) -> dict:
    """add/update videos to db"""

    t0 = time.time()
    logging.warning("add/update videos")

    for video in new_videos:
        id_video = str(video["id_video"]).strip()  # id video

        if (
            id_video not in old_videos_ids
        ) and new:  # add the video to the db if needed
            # enhance video

            try:
                with Session(engine) as session:
                    session.add(Video(**video))
                    session.commit()
                    payload["added"] += 1
            except Exception as e:
                logging.error(f"{e} - add video -> {video}")
                payload["errors_added"] += 1

        else:  # update the video
            # if old is False, do not update
            if not old:
                continue

            # randomize the update if needed
            if not random_:
                if not random.randint(0, 3):  # do not update each time
                    continue

            # enhance video
            if enhance_old:  # enhance video
                try:
                    video = _update_one_rss(video, detail=True, categ_1=True)
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

    payload["time_add_update_videos"] = round(time.time() - t0, 4)

    return payload


def reshape_payload(payload: dict, T0: float) -> dict:
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


def get_broken_videos(
    shuffle_=True,
    clean: bool = True,
) -> list[dict]:
    """return list of videos if broke (ie respond criterions such as category, duration etc)"""

    broken_videos = VideoQuery.all()

    f = (
        lambda i: (i["category"] == "Unknown")
        or (i["id_categ_1"] == "?")
        or (i["duration"] == DEFAULT_DURATION)
        or (i["thumbnail_video_url"] == DEFAULT_THUMBNAIL_VIDEO_URL)
    )
    broken_videos = [i for i in broken_videos if f(i)]

    if shuffle_:
        random.shuffle(broken_videos)

    if clean:
        broken_videos = clean_video_list(broken_videos)

    return broken_videos
