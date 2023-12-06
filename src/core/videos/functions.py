"""
main functions for core videos module 
main point of entry for videos module
=> update or fix old videos

"""

import os, sys, logging, time, random

from src.db import Session, engine

from src.helpers.helpers import make_now

from src.videos.models import Video

from src.core.videos.rss import CoreVideoRss
from src.core.videos.helpers import CoreVideoHelpers as CVH
from src.core.videos.queries import CoreVideoQueries as CVQ


def _update(
    new: bool = True,
    old: bool = True,
    random_: bool = True,
    enhance_old: bool = False,
    engine=engine,
) -> dict:
    """Update the database with new videos and old videos"""

    # timer
    T0 = time.time()

    # channel list ids and old videos
    channel_list_ids, time_load_channels = CVQ.channels_ids()
    old_videos_ids, time_load_videos = CVQ.old_videos_ids()

    # feeds new videos
    new_videos, time_get_feeds = CVH.scrap_feeds(
        channel_list_ids,
        scrap=True,
        detail=True,
        clean=True,
        parallel=True,
    )

    # payload
    payload = CVH.make_payload()
    payload["old_videos_count"] = len(old_videos_ids)
    payload["new_videos_count"] = len(new_videos)
    payload["time_load_channels"] = time_load_channels
    payload["time_load_videos"] = time_load_videos
    payload["time_get_feeds"] = time_get_feeds

    # add / update in db
    payload = CVH.add_update_db(
        new_videos=new_videos,
        old_videos_ids=old_videos_ids,
        payload=payload,
        new=new,
        old=old,
        random_=random_,
        enhance_old=enhance_old,
        engine=engine,
    )

    # reshape payload
    payload = CVH.reshape_payload(payload, T0)

    return payload


def _fix_old_videos(
    stop: int = 300,
    shuffle_: bool = False,
    engine=engine,
) -> dict:
    """Fix data inconsistant default values for old videos"""

    # get broken videos
    broken_videos = CVH.get_broken_videos(shuffle_=shuffle_)

    # limit if needed
    broken_videos = broken_videos[:stop]

    for i, video in enumerate(broken_videos):
        logging.info(f"video before fix {video}")

        # enhance video
        try:
            video = CoreVideoRss.update_one(video, detail=True, categ_1=True)
        except Exception as e:
            logging.error(f"enhance video - {e} - {video}")
            continue

        # update video
        id_video = video["id_video"]
        video["updated_at"] = make_now()

        logging.info(f"video after fix {video}")

        # add in db
        try:
            with Session(engine) as session:
                session.query(Video).filter_by(id_video=id_video).update(video)
                session.commit()
                # payload["updated"] += 1
        except Exception as e:
            logging.error(f"update video - {e} - {video}")
            # payload["errors_updated"] += 1

    # payload
    payload = {"ok": True}

    return payload


class CoreVideoFuncions:
    """Class for core videos functions
    public methods:
        - update
        - fix_old_videos
    """

    update = _update
    fix_old_videos = _fix_old_videos
