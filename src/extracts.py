import os, sys, logging, time
import requests
from bs4 import BeautifulSoup


def _alternative_rss_url(
    url,
    pattern={"type": "application/rss+xml"},
    verbose=1,
):
    """ """

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


def extract_rss_url(
    url, pattern={"type": "application/rss+xml"}, sleeper=0.2, verbose=1
):
    """ """

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("link", pattern)

    if not links:
        links = _alternative_rss_url(
            url=url,
            pattern=pattern,
            verbose=verbose,
        )

    if not links:
        return ""

    link = links[0].get("href")
    link = link.split("channel_id=")[1]

    if sleeper > 0:
        time.sleep(sleeper)

    if verbose >= 1:
        logging.warning(link)

    return link
