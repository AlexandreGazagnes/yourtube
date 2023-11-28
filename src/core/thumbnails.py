import os, logging

import requests

from src.params import get_params


def _request_rapid_api_details(id_video: str = "kJQP7kiw5Fk", MODE="dev") -> dict:
    """perform a request to rapid api to get the details of a video"""

    params = get_params(MODE=MODE)

    url = params["RAPIDAPI_URL"]
    if not url:
        raise ValueError(f"RAPIDAPI_URL is not defined : {params}")

    querystring = {"id": id_video, "hl": "en", "gl": "US"}

    headers = {
        "X-RapidAPI-Key": params.get("X-RapidAPI-Key"),
        "X-RapidAPI-Host": params.get("X-RapidAPI-Host"),
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()


def _clean_api_response(json: dict) -> dict:
    """clean the api response to get only the needed data"""

    thumbnail_url = json["thumbnails"][-2]["url"]
    category = json["category"]
    keywords = ",".join(json["keywords"][:5])

    return {
        "thumbnail_url": thumbnail_url,
        "category": category,
        "keywords": keywords,
    }


def enhance_video(video_dict, MODE="dev") -> dict:
    """get the thumbnail details of a video"""

    id_video = video_dict.get("id_video")

    json = _request_rapid_api_details(id_video=id_video, MODE=MODE)
    json = _clean_api_response(json)

    video_dict.update(json)

    return video_dict
