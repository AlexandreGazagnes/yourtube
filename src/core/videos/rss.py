import logging

from pandarallel import pandarallel

pandarallel.initialize()

import pandas as pd
import feedparser
from src.core.paths import RSS
from src.core.videos.extracts import extract_video_detail


def _clean_video_dict(video_dict, id_channel=""):
    """clean a video dict from a rss feed"""

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

    # TODO:
    # add thumbnail video url
    # add category
    # add keywords
    # add duration

    return {
        k: v
        for k, v in video_dict.items()
        if k
        not in [
            "yt_videoid",
        ]
    }


# def clean_entries(entries, id_channel=""):
#     """clean a list of entries from a rss feed"""

#     entries = [_clean_video_dict(i, id_channel) for i in entries]

#     return entries


def _extract_rss(id_channel):
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


# def _extract_rss_and_flatten(channel_list_ids):
#     """ """

#     feeds = [_extract_rss(i) for i in channel_list_ids]

#     new_videos = []
#     _ = [new_videos.extend(i) for i in feeds]

#     return new_videos


def build_rss(
    df: pd.DataFrame,
    extract_video_detail: bool = False,
    verbose: int = 1,
) -> pd.DataFrame:
    """build a dataframe from a list of channel ids"""

    # fill blanks if needed

    df.id_channel.fillna("", inplace=True)

    # list of list of feeds
    clean_entries = df.id_channel.parallel_apply(_extract_rss)

    # flatten the list of list of feeds
    li = []
    _ = [li.extend(i) for i in clean_entries]

    # build the dataframe
    df = pd.DataFrame(li)

    # published to datetime
    df["published"] = pd.to_datetime(df.published)

    # rename yt_videoid to id_video
    df.rename(columns={"yt_videoid": "id_video"}, inplace=True)

    if extract_video_detail:
        logging.warning(f"extracting video details for {len(df)} videos")
        details = df.parallel_apply(extract_video_detail, axis=1)
        df = pd.concat([df, details], axis=1, ignore_index=True)

    logging.info(f"rss feed built : {df}")

    return df
