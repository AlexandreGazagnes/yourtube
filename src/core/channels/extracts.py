import os, sys, logging, time
import requests
from bs4 import BeautifulSoup


from src.core.helpers import _manage_response


def _prepare_channel_url(channel_url):
    """prepare the channel url"""

    if not channel_url:
        # channel_url = "arte"
        return ""

    if not "youtube" in channel_url:
        channel_url = f"https://www.youtube.com/{channel_url}"

    if not "@" in channel_url:
        channel_url = channel_url.replace("youtube.com/", "youtube.com/@")

    return channel_url


def _outro(sleeper, verbose, var, value):
    """apply sleeper and verbose"""

    # sleeper
    if sleeper > 0.0001:
        time.sleep(sleeper)

    # verbose
    if verbose >= 1:
        logging.info(f"{var} : {value}")


def _alternative_rss_url(
    channel_url,
    pattern={"type": "application/rss+xml"},
    verbose=1,
):
    """alternative url extractor"""

    # new_channel_url = channel_url.replace("youtube.com/@", "youtube.com/")

    # response = requests.get(new_channel_url)
    # soup = BeautifulSoup(response.text, "html.parser")

    # links = soup.find_all("link", pattern)

    # if len(links) == 0:
    #     return ""

    # if verbose >= 2:
    #     logging.error("Alternative RSS URL")
    #     logging.error(f"base url {channel_url}")
    #     logging.error(f"alternative url {new_channel_url}")
    #     logging.error(f"links {links}")

    # return links

    pass


def _thumbnail(response, channel_url: str, sleeper: int = 0.1, verbose=1):
    """extract channel thumbnail from response"""

    # soup
    try:
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        logging.error(f"BeautifulSoup - {e} - {channel_url}")

    # extract channel thumbnail
    try:
        # link itemprop="thumbnailUrl"
        elem = soup.find("link", {"itemprop": "thumbnailUrl"})
        channel_thumbnail_url = elem.get("href")
    except Exception as e:
        logging.error(f"extract_thumbnail - {e} - {channel_url}")
        return ""

    # outro
    _outro(sleeper, verbose, "extract_thumbnail", extract_thumbnail)

    return channel_thumbnail_url


def _rss(
    response,
    channel_url,
    pattern={"type": "application/rss+xml"},
    sleeper: float = 0.1,
    verbose: int = 1,
):
    # soup and links
    try:
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("link", pattern)
    except Exception as e:
        logging.error(f"BeautifulSoup - {e} - {channel_url}")
        return ""

    # if not links:
    #     try:
    #         # if not links, try alternative url
    #         links = _alternative_rss_url(
    #             url=channel_url,
    #             pattern=pattern,
    #             verbose=verbose,
    #         )
    #     except Exception as e:
    #         logging.error(f"alternative_rss_url - {e} - {channel_url}")
    #         return ""

    # else return empty string
    if not links:
        logging.error(f"alternative_rss_url - {e} - {channel_url}")
        return ""

    # do extract rss links
    try:
        link = links[0].get("href")
        link = link.split("channel_id=")[1]
    except Exception as e:
        logging.error(f"extract rss from - {e} - {channel_url} - {links}")
        return ""

    _outro(sleeper, verbose, "link", link)

    return link


def extract_rss(
    channel_url: str | None,
    sleeper=0.1,
    verbose=1,
):
    """extract the rss link from the channel url"""

    # _prepare_channel_url
    channel_url = _prepare_channel_url(channel_url)
    if not channel_url:
        return ""

    # _manage_response
    response = _manage_response(channel_url, "channel_url")
    if not response:
        return ""

    # extract rss
    rss = _rss(response, channel_url, sleeper, verbose)

    return rss


def extract_thumbnail(
    channel_url: str | None,
    sleeper=0.1,
    verbose=1,
):
    """extract the channel thumbnail from the channel url"""

    # _prepare_channel_url
    channel_url = _prepare_channel_url(channel_url)
    if not channel_url:
        return ""

    # response
    response = _manage_response(channel_url, "channel_url")
    if not response:
        return ""

    # extract thumbnail
    thumbnail_url = _thumbnail(response, channel_url, sleeper, verbose)

    return thumbnail_url
