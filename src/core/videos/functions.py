"""
main functions for core videos module 
main point of entry for videos module
=> update or fix old videos

"""

# import logging, time, random
import os, sys, logging, time, random

# from random import shuffle

from src.db import Session, engine

# from src.params import get_params, params

# from src.helpers.queries import query_all
from src.helpers.helpers import make_now

from src.videos.models import Video

# from src.videos.queries import VideoQuery

# from src.channels.models import Channel
# from src.channels.queries import ChannelQuery

# from src.core.channels.extracts import extract_video_detail
from src.core.videos.rss import Rss
from src.core.videos.helpers import CoreVideoHelpers as CVH
from src.core.videos.queries import CoreVideoQueries as CVQ


def update(
    new: bool = True,
    old: bool = True,
    random_: bool = True,
    # enhance_new=True,
    enhance_old=False,
    engine=engine,
) -> dict:
    """Update the database with new videos and old videos"""

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

    # add update
    payload = CVH.add_update_db(
        new_videos=new_videos,
        old_videos_ids=old_videos_ids,
        payload=payload,
        new=new,
        old=old,
        random_=random_,
        # enhance_new=enhance_new,
        enhance_old=enhance_old,
        engine=engine,
    )

    payload = CVH.reshape_payload(payload, T0)
    return payload


def fix_old_videos(
    stop: int = 100,
    engine=engine,
) -> dict:
    """Fix data inconsistant default values for old videos"""

    # get broken videos
    broken_videos = CVH.get_broken_videos()

    for i, video in enumerate(broken_videos):
        # stop
        if stop == i:
            break

        # enhance video
        try:
            video = Rss.update_one(video, detail=True, categ_1=True)
        except Exception as e:
            logging.error(f"enhance video - {e} - {video}")
            continue

        # update video
        id_video = video["id_video"]
        video["updated_at"] = make_now()

        # add in db
        try:
            with Session(engine) as session:
                session.query(Video).filter_by(id_video=id_video).update(video)
                session.commit()
                # payload["updated"] += 1
        except Exception as e:
            logging.error(f"update video - {e} - {video}")
            # payload["errors_updated"] += 1

    payload = {"ok": True}
    return payload


# def fix_videos(stop=100, engine=None):
#     """ """

#     # if not engine:
#     #     params = get_params()
#     #     engine = Db.engine(params=params)

#     # # querry all videos from db
#     # video_list = VideoQuery.all(
#     #     limit=1_000_000,
#     #     last_days=100_000,
#     #     duration_max=100 * 3600,
#     #     duration_min=-1,
#     # )

#     # logging.warning(f"video_list {len(video_list)}\n\n")
#     # # filteer videos with 360 durration OR base image

#     # filter_ = lambda x: (x["duration"] in [DEFAULT_DURATION, -1]) or (
#     #     x["thumbnail_video_url"] == DEFAULT_THUMBNAIL_VIDEO_URL
#     # )

#     # video_list = [i for i in video_list if filter_(i)]

#     video_list = get_broken_videos()

#     logging.warning(f"video_list FILTERDED {len(video_list)}\n\n")

#     # for each video
#     for i, video in enumerate(video_list):
#         if i == stop:
#             logging.warning(f"stop at {i}\n\n")
#             break

#         if (
#             video["thumbnail_video_url"] == DEFAULT_THUMBNAIL_VIDEO_URL
#             or video["duration"] == DEFAULT_DURATION
#         ):
#             logging.warning(f"video {video}\n\n")
#             logging.warning("go to  fix it \n\n")

#             new_video_dict = extract_video_detail(video["id_video"])

#             logging.warning(f"new_video_dict {new_video_dict}\n\n")

#             if not new_video_dict:
#                 logging.warning(f"nothing to fix, new_video {new_video_dict} \n\n")
#                 continue

#             # else
#             video["duration"] = new_video_dict["duration"]
#             video["thumbnail_video_url"] = new_video_dict["thumbnail_video_url"]

#             # clean
#             video = {
#                 k: v for k, v in video.items() if k in Video.__table__.columns.keys()
#             }
#             video["updated_at"] = make_now()

#             # # item DB
#             # video = Video(**video)
#             # logging.warning(f"video OBJECT {video}\n\n")

#             # check video items
#             logging.warning(f"video AFTER CLEAN {video}\n\n")
#             try:
#                 with Session(engine) as session:
#                     # pre clean video cols

#                     # update video
#                     session.query(Video).filter(
#                         Video.id_video == video["id_video"]
#                     ).update(video)

#                     # commit
#                     session.commit()

#                     # logging
#                     logging.warning(f"video updated in db {video}\n\n")
#             except Exception as e:
#                 logging.error(f"error update in db {e}  for video {video}\n\n")


# # if __name__ == "__main__":
# #     """ """
