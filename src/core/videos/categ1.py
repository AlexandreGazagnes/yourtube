from src.core.videos.queries import query_one

import logging


winamax_dict = {
    "poker": "Poker",
    "d'un pro": "Poker",
    "ufc": "Bagarre",
    "tennis": "Sport",
    "uber eats": "Foot",
    "foot": "Foot",
    "ligue 2": "Foot",
    "ligue 1": "Foot",
    "f1": "F1",
    "psg": "Foot",
    "premier ligue": "Foot",
    "saudi pro league": "Foot",
    "ligua europa": "Foot",
    "ligue des champions": "Foot",
    "formule 2": "F1",
    "formule 1": "F1",
    "bkt": "Foot",
}

canalplus_dict = {
    # "poker": "Poker",
    "ufc": "Bagarre",
    "tennis": "Sport",
    "uber eats": "Foot",
    "foot": "Foot",
    "ligue 2": "Foot",
    "ligue 1": "Foot",
    "f1": "F1",
    "psg": "Foot",
    "premier ligue": "Foot",
    "saudi pro league": "Foot",
    "ligua europa": "Foot",
    "ligue des champions": "Foot",
    "formule 2": "F1",
    "formule 1": "F1",
    "bkt": "Foot",
}


rmc_sport_dict = {
    "poker": "Poker",
    "ufc": "Bagarre",
    "tennis": "Sport",
    "uber eats": "Foot",
    "foot": "Foot",
    "ligue 2": "Foot",
    "ligue 1": "Foot",
    "f1": "F1",
    "psg": "Foot",
    "premier ligue": "Foot",
    "saudi pro league": "Foot",
    "ligua europa": "Foot",
    "ligue des champions": "Foot",
    "formule 2": "F1",
    "formule 1": "F1",
    "bkt": "Foot",
}


def _impute(title: str, value_dict: dict) -> str:
    """find categ from title and value_dict"""

    for key, value in value_dict.items():
        if key in title.lower():
            return value

    return "Sport"


def add_categ1(video_dict: dict) -> dict:
    """ """

    # check if id_video and id_channel are present
    if (not video_dict.get("id_video", None)) or (
        not video_dict.get("id_channel", None)
    ):
        logging.error(f"missing id_video or id_channel in video_dict: {video_dict}")
        video_dict["id_categ_1"] = "?"
        return video_dict

    # extra data
    data = query_one(video_dict["id_video"], video_dict["id_channel"])
    if not data:
        logging.error(f"no data from query_one for video_dict: {video_dict}")
        video_dict["id_categ_1"] = "?"
        return video_dict

    pairs = {
        "winamax": winamax_dict,
        "canalplus": canalplus_dict,
        "rmc sport": rmc_sport_dict,
    }

    # find the relevand channel
    for key, value_dict in pairs.items():
        # if key map the name of the channel
        if key in data["name"].lower() or key in data["author"].lower():
            # impute categ 1 with specific dictionnary
            id_categ_1 = _impute(video_dict["title"], value_dict)
            video_dict["id_categ_1"] = id_categ_1
            return video_dict

    # if no match
    video_dict["id_categ_1"] = data.get("id_categ_1", "?")
    return video_dict
