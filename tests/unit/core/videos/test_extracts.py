import logging

from random import shuffle

from src.core.videos.extracts import _extract_video_detail
from src.videos.queries import VideoQuery


class TestExtract:
    """ """

    def test_extract_video_detail(self):
        """ """

        video_list = VideoQuery.all()
        shuffle(video_list)

        video = video_list[0]
        id_video = video["id_video"]

        # id_video = "Pgb8hubPATs"

        logging.info(f"id_video : {id_video}")
        logging.info(f"video before : {video}")
        data = _extract_video_detail(id_video)

        assert isinstance(data, dict)
        assert data

        logging.info(f"video after : {data}")

    def test_extract_video_detail_veracity(self):
        """ """

        # video_list = VideoQuery.all()
        # shuffle(video_list)

        # video = video_list[0]
        # id_video = video["id_video"]

        id_video = "R768GQu3AZ4"

        logging.info(f"id_video : {id_video}")
        # logging.info(f"video before : {video}")
        data = _extract_video_detail(id_video)

        assert isinstance(data, dict)
        assert data

        logging.info(f"video after : {data}")
