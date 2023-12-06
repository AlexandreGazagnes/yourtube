# import logging, time, random
import os, sys, logging, time, random
from random import shuffle

from src.db import Session, engine

from src.params import get_params, params

from src.helpers.queries import query_all
from src.helpers.helpers import make_now

from src.videos.models import Video
from src.videos.queries import VideoQuery

from src.channels.models import Channel
from src.channels.queries import ChannelQuery

from src.core.channels.extracts import extract_video_detail


DEFAULT_THUMBNAIL_VIDEO_URL = "https://i.ytimg.com/vi/kJQP7kiw5Fk/hqdefault.jpg?sqp=-oaymwEcCPYBEIoBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLC7mQvF1DbgLkymd5TjUQjWLbaJ3A"
DEFAULT_DURATION = 360


def _update(
    new=True,
    old=True,
    random_=True,
    enhance_new=True,
    enhance_old=False,
    engine=engine,
):
    """Update the database with new videos and old videos"""

    T0 = time.time()

    # channel list ids and old videos
    channel_list_ids, time_load_channels = HomeHelpers.load_channels_ids()
    old_videos_ids, time_load_videos = HomeHelpers.load_old_videos_ids()

    # feeds new videos
    new_videos, time_get_feeds = HomeHelpers.load_feeds(channel_list_ids)
    new_videos = HomeHelpers.clean_videos(new_videos)

    # payload
    payload = HomeHelpers.make_payload()
    payload["old_videos_count"] = len(old_videos_ids)
    payload["new_videos_count"] = len(new_videos)
    payload["time_load_channels"] = time_load_channels
    payload["time_load_videos"] = time_load_videos
    payload["time_get_feeds"] = time_get_feeds

    # add update
    payload = HomeHelpers.add_update_db(
        new_videos=new_videos,
        old_videos_ids=old_videos_ids,
        payload=payload,
        new=new,
        old=old,
        random_=random_,
        enhance_new=enhance_new,
        enhance_old=enhance_old,
    )

    payload = HomeHelpers.reshape_payload(payload, T0)
    return payload


def _fix_old_videos(engine=engine):
    """Fix data inconsistant default values for old videos"""

    broken_videos = HomeHelpers.get_broken_videos()
    broken_videos = HomeFunctions.clean_videos(broken_videos)

    for i, video in enumerate(broken_videos):
        # enhance video
        try:
            video = enhance_video(video)
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


def fix_videos(stop=100, engine=None):
    """ """

    # if not engine:
    #     params = get_params()
    #     engine = Db.engine(params=params)

    # querry all videos from db
    video_list = VideoQuery.all(
        limit=1_000_000,
        last_days=100_000,
        duration_max=100 * 3600,
        duration_min=-1,
    )

    logging.warning(f"video_list {len(video_list)}\n\n")
    # filteer videos with 360 durration OR base image

    filter_ = lambda x: (x["duration"] in [DEFAULT_DURATION, -1]) or (
        x["thumbnail_video_url"] == DEFAULT_THUMBNAIL_VIDEO_URL
    )

    video_list = [i for i in video_list if filter_(i)]

    logging.warning(f"video_list FILTERDED {len(video_list)}\n\n")

    # for each video
    for i, video in enumerate(video_list):
        if i == stop:
            logging.warning(f"stop at {i}\n\n")
            break

        if (
            video["thumbnail_video_url"] == DEFAULT_THUMBNAIL_VIDEO_URL
            or video["duration"] == DEFAULT_DURATION
        ):
            logging.warning(f"video {video}\n\n")
            logging.warning("go to  fix it \n\n")

            new_video_dict = extract_video_detail(video["id_video"])

            logging.warning(f"new_video_dict {new_video_dict}\n\n")

            if not new_video_dict:
                logging.warning(f"nothing to fix, new_video {new_video_dict} \n\n")
                continue

            # else
            video["duration"] = new_video_dict["duration"]
            video["thumbnail_video_url"] = new_video_dict["thumbnail_video_url"]

            # clean
            video = {
                k: v for k, v in video.items() if k in Video.__table__.columns.keys()
            }
            video["updated_at"] = make_now()

            # # item DB
            # video = Video(**video)
            # logging.warning(f"video OBJECT {video}\n\n")

            # check video items
            logging.warning(f"video AFTER CLEAN {video}\n\n")
            try:
                with Session(engine) as session:
                    # pre clean video cols

                    # update video
                    session.query(Video).filter(
                        Video.id_video == video["id_video"]
                    ).update(video)

                    # commit
                    session.commit()

                    # logging
                    logging.warning(f"video updated in db {video}\n\n")
            except Exception as e:
                logging.error(f"error update in db {e}  for video {video}\n\n")


# if __name__ == "__main__":
#     """ """
