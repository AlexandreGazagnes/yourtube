import logging
from random import shuffle

from src.videos.queries import VideoQuery

from src.core.videos.extracts import _extract_video_detail


class TestExtract:
    """class TestExtract"""

    def test_extract_video_detail(self, verbose: bool = True):
        """test _extract_video_detail"""

        # get random video
        video_list = VideoQuery.all()
        shuffle(video_list)

        # select one
        video = video_list[0]
        id_video = video["id_video"]

        if verbose:
            logging.info(f"id_video : {id_video}")
            logging.info(f"video before : {video}")

        data = _extract_video_detail(id_video)

        assert isinstance(data, dict)
        assert data

        if verbose:
            logging.info(f"video after : {data}")

    def test_extract_video_detail_veracity(self, verbose: bool = True):
        """test_extract_video_detail_veracity"""

        # find specific id_video
        id_video = "R768GQu3AZ4"
        if verbose:
            logging.info(f"id_video : {id_video}")

        data = _extract_video_detail(id_video)

        assert isinstance(data, dict)
        assert data

        if verbose:
            logging.info(f"video after : {data}")
