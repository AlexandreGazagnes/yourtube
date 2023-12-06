import logging

from pandarallel import pandarallel

pandarallel.initialize()

import pandas as pd
import feedparser
from src.core.paths import RSS
from src.core.videos.categ1 import manage_categ1
from src.core.videos.extracts import extract_video_detail, update_video_detail


def _clean_video_dict(video_dict, id_channel=""):
    """clean a video dict from a rss feed"""

    # accepted_keys
    accepted_keys = [
        # "link",
        "yt_videoid",
        "title",
        "author",
        "published",
        "media_starrating",
        "media_statistics",
        # "media_content",
        # "summary",
        # "summary_detail",
        # "media_community",
    ]

    # update dict
    video_dict = {i: j for i, j in video_dict.items() if i in accepted_keys}

    # id_video
    video_dict["id_video"] = video_dict["yt_videoid"]

    # media_starrating
    media_starrating = video_dict.get("media_starrating", {})
    video_dict["votes"] = int(media_starrating.get("count", -1))
    video_dict["stars"] = float(media_starrating.get("average", -1.0))
    # video_dict["stars"] = int(video_dict["stars"])

    # media_statistics
    video_dict["views"] = int(video_dict.get("media_statistics", {}).get("views", 0))

    # clean dict
    video_dict = {
        k: v
        for k, v in video_dict.items()
        if k not in ["media_starrating", "media_statistics"]
    }

    # id_channel
    video_dict["id_channel"] = id_channel

    # clean title
    video_dict["title"] = video_dict["title"][:100]

    # "published"
    video_dict["published"] = pd.to_datetime(video_dict["published"])

    return {
        k: v
        for k, v in video_dict.items()
        if k
        not in [
            "yt_videoid",
        ]
    }


def _scrap_one_rss(id_channel: str):
    """extract the rss feed from a channel id"""

    if not id_channel:
        return []

    # feeds
    feeds = feedparser.parse(RSS + id_channel)

    # entries
    entries = feeds.entries

    entries_cleaned = [_clean_video_dict(i, id_channel) for i in entries]
    # entries_cleaned = clean_entries(entries, id_channel=id_channel)

    return entries_cleaned


def _scrap_rss_list(
    channel_list: list[str],
    parallel: bool = True,
    verbose: int = 1,
) -> list[dict]:
    """ """

    channel_list = pd.Series(channel_list).fillna("")

    if parallel:
        clean_entries = channel_list.parallel_apply(_scrap_one_rss)
    else:
        clean_entries = channel_list.apply(_scrap_one_rss)

    # flatten the list of list of feeds
    li = []
    _ = [li.extend(i) for i in clean_entries]

    return li


def _update_rss_list(
    rss_list: list[dict],
    video_detail=False,
    categ_1=False,
    parallel=True,
    verbose: int = 1,
) -> list[dict]:
    """ " """

    if not rss_list:
        logging.error(f"rss_list is empty : {rss_list}")
        return []

    rss_list = pd.Series(rss_list).fillna({})

    # logging.info(f"type rss_list : {type(rss_list)}")
    # logging.info(f"rss_list : {rss_list}")
    # input("stop here")

    if video_detail:
        if parallel:
            updated_rss_list = rss_list.parallel_apply(update_video_detail)
        else:
            updated_rss_list = rss_list.apply(update_video_detail)

    # logging.info(f"type updated_rss_list : {type(updated_rss_list)}")

    if categ_1:
        if video_detail:
            rss_list = updated_rss_list.copy()

        if parallel:
            updated_rss_list = rss_list.parallel_apply(manage_categ1)
        else:
            updated_rss_list = rss_list.apply(manage_categ1)

    # logging.critical(f"type updated_rss_list : {type(updated_rss_list)}")

    # raise ArithmeticError("stop here")

    return updated_rss_list.values.tolist()


def build_rss_df(
    channel_list: list,
    video_detail: bool = False,
    categ_1: bool = False,
    verbose: int = 1,
    parallel=True,
) -> pd.DataFrame:
    """build a dataframe from a list of channel ids"""

    # fill blanks if needed

    rss_list = _scrap_rss_list(channel_list)

    # extract video details
    if video_detail:
        logging.warning(f"extracting video details for {len(df)} videos")
        if parallel:
            details = df.id_video.parallel_apply(update_video_detail)
        else:
            details = df.id_video.apply(update_video_detail)

        # DF
        details = pd.DataFrame(details.values.tolist())
        df = pd.concat([df, details], axis=1)

    # update categ1
    if categ_1:
        list_new_dict = [manage_categ1(v.to_dict()) for k, v in df.iterrows()]
        df = pd.DataFrame(list_new_dict)

    logging.info(f"rss feed built : {df}")

    return df
