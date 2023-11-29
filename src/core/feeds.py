import pandas as pd
import feedparser
from src.core.paths import RSS


def clean_video_dict(video_dict, id_channel=""):
    """clean a video dict from a rss feed"""

    keys = [
        # "link",
        "yt_videoid",
        "title",
        "author",
        "published",
        # "media_content",
        # "summary",
        # "summary_detail",
        "media_starrating",
        "media_statistics",
        # "media_community",
    ]

    video_dict = {i: j for i, j in video_dict.items() if i in keys}

    media_starrating = video_dict.get("media_starrating", {})
    video_dict["stars"] = int(media_starrating.get("count", 0)) * float(
        media_starrating.get("average", 0)
    )
    video_dict["stars"] = int(video_dict["stars"])
    video_dict["views"] = int(video_dict.get("media_statistics", {}).get("views", 0))

    video_dict = {
        k: v
        for k, v in video_dict.items()
        if k not in ["media_starrating", "media_statistics"]
    }

    video_dict["id_channel"] = id_channel

    return video_dict


def clean_entries(entries, id_channel=""):
    """clean a list of entries from a rss feed"""

    entries = [clean_video_dict(i, id_channel) for i in entries]

    return entries


def extract_rss(id_channel):
    """extract the rss feed from a channel id"""

    if not id_channel:
        return []

    feeds = feedparser.parse(RSS + id_channel)
    entries = feeds.entries
    entries_cleaned = clean_entries(entries, id_channel=id_channel)

    return entries_cleaned


def extract_rss_and_flatten(channel_list_ids):
    """ """

    feeds = [extract_rss(i) for i in channel_list_ids]

    new_videos = []
    _ = [new_videos.extend(i) for i in feeds]

    return new_videos


def build_rss(df: pd.DataFrame):
    """build a dataframe from a list of channel ids"""

    df.id_channel.fillna("", inplace=True)
    clean_entries = df.id_channel.parallel_apply(extract_rss)

    li = []
    _ = [li.extend(i) for i in clean_entries]

    df = pd.DataFrame(li)
    df["published"] = pd.to_datetime(df.published)

    df.rename(columns={"yt_videoid": "id_video"}, inplace=True)

    return df
