import logging

import requests

from bs4 import BeautifulSoup


def extract_video_detail(
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
    # to do use _manage_response
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
    duration = ""
    try:
        pattern = '"lengthSeconds": "'.replace(" ", "")
        _duration = response.text.split(pattern)[1][:100]
        _duration = int(_duration.split('"')[0].strip())
        duration = _duration
    except Exception as e:
        logging.error(f"duration - {e} - {video_url} - duration set to -{duration}")

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

    # # channel Thumbnail
    #   pattern = '"channelThumbnail": { "thumbnails": [{ "url": '.replace(" ", "")
    #   channel_thumbnail_url = response.text.split(pattern)[1][:300]
    #   channel_thumbnail_url = channel_thumbnail_url[1:].split('"')[0]

    # keywords
    keywords = ""
    try:
        _keywords = soup.find("meta", {"name": "keywords"}).get("content")[:100]
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

    return data


def update_video_detail(video_dict: dict) -> dict:
    """ """

    logging.info(f"candidate to update_video_detail {video_dict}")

    if not isinstance(video_dict, dict):
        logging.error(f"error attribute video_dict is not a dict : {video_dict}")
        # raise AttributeError(f"error attribute video_dict is not a dict : {video_dict}")

    # video_url
    id_video = video_dict.get("id_video", None)

    if not id_video:
        logging.error(f"error attribute id_video is not a str : {id_video}")
        # raise AttributeError(f"error attribute id_video is not a str : {id_video}")

    # extract video detail
    video_detail = extract_video_detail(id_video)

    # update video dict
    video_dict.update(video_detail)

    return video_dict
