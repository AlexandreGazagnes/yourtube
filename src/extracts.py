import os, sys, logging, time
import requests
from bs4 import BeautifulSoup


def extract_rss_url(
    url, pattern={"type": "application/rss+xml"}, sleeper=0.2, verbose=1
):
    """ """

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("link", pattern)

    if len(links) == 0:
        return ""

    link = links[0].get("href")
    link = link.split("channel_id=")[1]

    if sleeper > 0:
        time.sleep(sleeper)

    if verbose:
        logging.warning(link)

    return link
