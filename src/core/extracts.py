import os, sys, logging, time
import requests
from bs4 import BeautifulSoup


def _alternative_rss_url(
    channel_url,
    pattern={"type": "application/rss+xml"},
    verbose=1,
):
    """alternative url extractor"""

    new_channel_url = channel_url.replace("youtube.com/@", "youtube.com/")

    response = requests.get(new_channel_url)
    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("link", pattern)

    if len(links) == 0:
        return ""

    if verbose >= 2:
        logging.error("Alternative RSS URL")
        logging.error(f"base url {channel_url}")
        logging.error(f"alternative url {new_channel_url}")
        logging.error(f"links {links}")

    return links


def extract_rss_from(
    channel_url: str | None,
    pattern={"type": "application/rss+xml"},
    sleeper=0.1,
    verbose=1,
):
    """extract the rss link from the channel url"""

    if not channel_url:
        channel_url = "arte"

    if not "youtube" in channel_url:
        channel_url = f"https://www.youtube.com/{channel_url}"

    if not "@" in channel_url:
        channel_url = channel_url.replace("youtube.com/", "youtube.com/@")

    # response
    try:
        response = requests.get(channel_url)
        if not response.ok:
            logging.error(f"requests - {response.status_code} - {channel_url}")
            return ""
    except Exception as e:
        logging.error(f"requests - {e} - {channel_url}")
        return ""

    # soup and links
    try:
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("link", pattern)
    except Exception as e:
        logging.error(f"BeautifulSoup - {e} - {channel_url}")
        return ""

    if not links:
        try:
            # if not links, try alternative url
            links = _alternative_rss_url(
                url=channel_url,
                pattern=pattern,
                verbose=verbose,
            )
        except Exception as e:
            logging.error(f"alternative_rss_url - {e} - {channel_url}")
            return ""

    # else return empty string
    if not links:
        return ""

    # do extract rss links
    try:
        link = links[0].get("href")
        link = link.split("channel_id=")[1]
    except Exception as e:
        logging.error(f"extract rss from - {e} - {channel_url} - {links}")
        return ""

    if sleeper > 0.0001:
        time.sleep(sleeper)

    if verbose >= 1:
        logging.warning(link)

    return link


def extract_channel_thumbnail(
    channel_url: str | None,
    sleeper=0.1,
    verbose=1,
):
    """extract the channel thumbnail from the channel url"""

    if not channel_url:
        channel_url = "arte"

    if not "youtube" in channel_url:
        channel_url = f"https://www.youtube.com/{channel_url}"

    if not "@" in channel_url:
        channel_url = channel_url.replace("youtube.com/", "youtube.com/@")

    # response
    try:
        response = requests.get(channel_url)

        if not response.ok:
            logging.error(f"requests - {response.status_code} - {channel_url}")
            return ""

    except Exception as e:
        logging.error(f"requests - {e} - {channel_url}")
        return ""

    # soup
    try:
        soup = BeautifulSoup(response.text, "html.parser")

        # link itemprop="thumbnailUrl"
        elem = soup.find("link", {"itemprop": "thumbnailUrl"})
        channel_thumbnail_url = elem.get("href")
        return channel_thumbnail_url

    except Exception as e:
        logging.error(f"BeautifulSoup - {e} - {channel_url}")
        return ""

    return ""


def extract_video_detail(
    video_url: str | None,
    sleeper=0.1,
    verbose=1,
):
    """extract the video detail from the video url"""

    if not video_url:
        video_url = "iE_VBlqfVXs"

    if not "youtube" in video_url:
        video_url = f"https://www.youtube.com/watch?v={video_url}"

    # response
    try:
        response = requests.get(video_url)
        if not response.ok:
            logging.error(f"requests - {response.status_code} - {video_url}")
            return {}
    except Exception as e:
        logging.error(f"requests - {e} - {video_url}")
        return {}

    # soup
    try:
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logging.error(f"BeautifulSoup - {e} - {video_url}")
        return {}

    # duration
    pattern = '"lengthSeconds": "'.replace(" ", "")
    duration = response.text.split(pattern)[1][:100]
    duration = int(duration.split('"')[0].strip())

    # video_thumbnail_url
    pattern = '"thumbnail": { "thumbnails": [{ "url": '.replace(" ", "")
    video_thumbnail_url = response.text.split(pattern)[1][:300]
    video_thumbnail_url = video_thumbnail_url[1:].split('"')[0]

    # # channel Thumbnail
    # pattern = '"channelThumbnail": { "thumbnails": [{ "url": '.replace(" ", "")
    # channel_thumbnail_url = response.text.split(pattern)[1][:300]
    # channel_thumbnail_url = channel_thumbnail_url[1:].split('"')[0]

    # keywords
    keywords = soup.find("meta", {"name": "keywords"}).get("content")[:100]

    # category
    # "category": "
    pattern = '"category": "'.replace(" ", "")
    category = response.text.split(pattern)[1][:100]
    category = category.split('"')[0].strip()

    return {
        "thumbnail_video_url": video_thumbnail_url,
        "category": category,
        "keywords": keywords[:100],
        "duration": duration,
    }
