"""
Scraping module 
get a video url page and request soup add detail to the video dict
"""

import logging

import requests

from bs4 import BeautifulSoup


def _extract_video_detail(
    video_url_or_id: str,
    sleeper: float = 0.1,
    verbose: int = 1,
) -> dict:
    """extract the video detail from the video url by scraping the page"""

    # update video url if neeeded
    prefix = "https://www.youtube.com/watch?v="
    video_url = (
        video_url_or_id
        if "youtube" in video_url_or_id
        else f"{prefix}{video_url_or_id}"
    )

    # response
    # TODO use _manage_response
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
    # TODO understand why the pattern is not working sometimes
    duration, duration_1, duration_2 = "", "", ""
    try:
        pattern = '"lengthSeconds": "'.replace(" ", "")
        duration_1 = response.text.split(pattern)[1][:100]
        duration_2 = int(duration_1.split('"')[0].strip())
        duration = duration_2
    except Exception as e:
        logging.error(
            f"duration - {e} - {video_url} - duration 1,2,3 {duration_1} - {duration_2} -> {duration} "
        )

    # video_thumbnail_url
    video_thumbnail_url = ""
    try:
        video_thumbnail_url = "none"
        pattern = '"thumbnail": { "thumbnails": [{ "url": '.replace(" ", "")
        _video_thumbnail_url = response.text.split(pattern)[1][:300]
        _video_thumbnail_url = _video_thumbnail_url[1:].split('"')[0]
        video_thumbnail_url = _video_thumbnail_url
    except Exception as e:
        logging.error(
            f"video_thumbnail_url - {e} - {video_url} - video_thumbnail_url set to -{video_thumbnail_url}"
        )

    # keywords
    keywords = ""
    try:
        _keywords = soup.find("meta", {"name": "keywords"}).get("content")[:100]
        # TODO add split and strip method for cleaner keywords
        keywords = _keywords
    except Exception as e:
        logging.error(f"keywords - {e} - {video_url} - keywords set to -{keywords}")

    # category
    category = ""
    try:
        pattern = '"category": "'.replace(" ", "")
        _category = response.text.split(pattern)[1][:100]
        _category = _category.split('"')[0].strip()
        category = _category
    except Exception as e:
        logging.error(f"category - {e} - {video_url} - category set to -{category}")

    data = {
        "thumbnail_video_url": video_thumbnail_url,
        "category": category,
        "keywords": keywords[:100],
        "duration": duration,
    }

    data = {k: v for k, v in data.items() if v}

    logging.info(f"video detail extracted {data}")

    return data


def _update_video_detail(video_dict: dict) -> dict:
    """based on a video dict update the video detail and retrurn new better video dict"""

    logging.info(f"candidate to _update_video_detail {video_dict}")

    # if not a dict
    if not isinstance(video_dict, dict):
        logging.error(f"error attribute video_dict is not a dict : {video_dict}")
        return video_dict

    # video_url
    id_video = video_dict.get("id_video", None)

    # if not id_video
    if not id_video:
        logging.error(f"error attribute id_video is not a str : {id_video}")
        return video_dict

    # extract video detail
    video_detail = _extract_video_detail(id_video)

    # update video dict
    video_dict.update(video_detail)

    logging.info(f"proceed after _update_video_detail {video_dict}")

    return video_dict


class CoreVideoExtracts:
    """class CoreVideoExtracts
    public methods:
        - update_video_detail
    """

    update_video_detail = _update_video_detail
