import logging

from src.core.videos.extracts import extract_video_detail


class TestExtract:
    """ """

    def test_extract_video_detail(self):
        """ """

        id_video = "Pgb8hubPATs"
        data = extract_video_detail(id_video)

        assert isinstance(data, dict)
        assert data

        logging.info(data)
