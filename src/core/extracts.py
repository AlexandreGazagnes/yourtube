import os, sys, logging, time
import requests
from bs4 import BeautifulSoup


def _alternative_rss_url(
    url,
    pattern={"type": "application/rss+xml"},
    verbose=1,
):
    """alternative url extractor"""

    url = url.split("/")
    url[-1] = "@" + url[-1]
    new_url = "/".join(url)

    response = requests.get(new_url)
    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("link", pattern)

    if len(links) == 0:
        return ""

    if verbose >= 2:
        logging.error("Alternative RSS URL")
        logging.error(f"base url {url}")
        logging.error(f"alternative url {new_url}")
        logging.error(f"links {links}")

    return links


def extract_rss_from(
    channel_url,
    pattern={"type": "application/rss+xml"},
    sleeper=0.1,
    verbose=1,
):
    """extract the rss link from the channel url"""

    if not "youtube" in channel_url:
        channel_url = f"https://www.youtube.com/{channel_url}"

    # response
    try:
        response = requests.get(channel_url)
    except Exception as e:
        logging.error(f"requests - {e} - {channel_url}")
        return ""

    if not response.ok:
        logging.error(f"requests - {response.status_code} - {channel_url}")
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
    channel_url: str,
    pattern={},
    sleeper=0.1,
    verbose=1,
):
    """extract the channel thumbnail from the channel url"""

    # # response
    # try:
    #     response = requests.get(channel_url)
    # except Exception as e:
    #     logging.error(f"requests - {e} - {channel_url} - {links}")
    #     return ""

    # # soup and links
    # try:
    #     soup = BeautifulSoup(response.text, "html.parser")
    #     links = soup.find_all("link", pattern)
    # except Exception as e:
    #     logging.error(f"BeautifulSoup - {e} - {channel_url}")
    #     return ""

    raise NotImplementedError("extract_channel_thumbnail")
