import pandas as pd
import feedparser
from src.paths import RSS


def clean_video_dict(video_dict, id_channel=""):
    """ """

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
        i: j
        for i, j in video_dict.items()
        if i not in ["media_starrating", "media_statistics"]
    }

    video_dict["id_channel"] = id_channel

    return video_dict


def clean_entries(entries, id_channel=""):
    """ """

    entries = [clean_video_dict(i, id_channel) for i in entries]

    return entries


def extract_rss(rss_url):
    """ """

    if not rss_url:
        return []

    feeds = feedparser.parse(RSS + rss_url)
    entries = feeds.entries
    entries_cleaned = clean_entries(entries, id_channel=rss_url)

    return entries_cleaned


def build_rss(df: pd.DataFrame):
    """ """

    df.rss_url.fillna("", inplace=True)
    clean_entries = df.rss_url.parallel_apply(extract_rss)

    li = []
    _ = [li.extend(i) for i in clean_entries]

    df = pd.DataFrame(li)
    df["published"] = pd.to_datetime(df.published)

    df.rename(columns={"yt_videoid": "id_video"}, inplace=True)

    return df
