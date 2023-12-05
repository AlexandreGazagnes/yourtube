import logging

import pytest

from src.core.videos.queries import query_one
from src.core.videos.categ1 import _find_cate1, pairs
from src.db import Session, engine

from src.params import get_params, params
from src.db import Db

# verbose = True


class TestCateg1:
    """Test categ1"""

    def test_find_categ1(self, verbose: bool = True):
        """test"""

    data = {
        "name": "winamax",
        "author": "winamax",
    }
    video_dict = {
        "title": "dans la tête d'un pro",
    }
    new_video_dict = _find_cate1(video_dict, data, pairs)

    assert new_video_dict["id_categ_1"].lower() == "poker"
