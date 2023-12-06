"""
module about adding good categ1 to video_dict 
regarding the channel name/categ1 or overdire with keywords 
from the title of video
"""

from src.core.videos.queries import query_one
from collections import OrderedDict
import logging


winamax_dict = OrderedDict(
    {
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
        "manchester city": "Foot",
        "tottenham": "Foot",
        "liverpool": "Foot",
        "barca": "Foot",
        "barcelone": "Foot",
        "real madrid": "Foot",
        "inter milan": "Foot",
        "real": "Foot",
        "barca": "Foot",
        "ac milan": "Foot",
        "arsenal": "Foot",
        "al-Hilal": "Foot",
        "al-Nassr": "Foot",
        "man city": "Foot",
        "athlético": "Foot",
        "athletico": "Foot",
        "euro 2024": "Foot",
        "but": "Foot",
    }
)

canalplus_dict = winamax_dict

rmc_sport_dict = winamax_dict

pairs = {
    "winamax": winamax_dict,
    "canalplus": canalplus_dict,
    "canal +": canalplus_dict,
    "canal+": canalplus_dict,
    "rmc sport": rmc_sport_dict,
    "rmcsport": rmc_sport_dict,
}


def _impute(title: str, value_dict: dict) -> str:
    """find categ from title and value_dict"""

    for key, value in value_dict.items():
        if key in title.lower():
            return value

    return "Sport"


def _find_cate1(video_dict, data, pairs):
    """ """

    ##################" ATTENTION POUR QUE CA MARCHE IL FAUT QUE CA SOIT DEJA EN BDD !!!!!!!!!!!!!!!!!!!"

    id_categ_1 = ""

    # find the relevand channel
    for key, value_dict in pairs.items():
        # if key map the name of the channel
        if key in data["name"].lower() or key in data["author"].lower():
            # impute categ 1 with specific dictionnary
            id_categ_1 = _impute(video_dict["title"], value_dict)
            # video_dict["id_categ_1"] = id_categ_1
            # return video_dict

    video_dict["id_categ_1"] = id_categ_1 if id_categ_1 else data.get("id_categ_1", "?")

    return video_dict


def _manage_categ1(video_dict: dict) -> dict:
    """ """

    if not isinstance(video_dict, dict):
        raise AttributeError(f"error attribute video_dict is not a dict : {video_dict}")

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

    new_video_dict = _find_cate1(video_dict, data, pairs)

    return new_video_dict


class Categ1:
    manage_categ1 = _manage_categ1