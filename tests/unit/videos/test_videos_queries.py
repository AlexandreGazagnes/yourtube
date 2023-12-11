import logging, json
from pprint import pformat

from src.videos.queries import (
    _query_videos_count,
    _query_all_ids_videos,
    _query_all_videos,
    _query_videos_by_user,
    _query_videos_by_channel,
)


class TestVideosQueries:
    """test user queries"""

    def test_query_video_count(self, verbose: bool = True, csv: bool = True):
        """test counts"""

        payload = _query_videos_count()

        # assert isinstance(payload, dict)
        # assert "users" in payload.keys()
        # assert isinstance(payload["users"], int)

        if verbose:
            logging.info(payload)

    def test_query_all_id_videos(self, verbose: bool = True, csv: bool = True):
        """test preferences"""

        result = _query_all_ids_videos()

        # assert isinstance(payload, dict)
        # assert "id_user" in payload.keys()
        # assert isinstance(payload["id_user"], int)

        result = result[:5]
        if verbose:
            logging.info(pformat(result))

    def test_query_video_by_user(self, verbose: bool = True, csv: bool = True):
        """test channels"""

        id_user = 3
        result, _ = _query_videos_by_user(id_user=id_user)

        # assert isinstance(payload, list)
        # assert isinstance(payload[0], dict)
        # assert "id_channel" in payload[0].keys()
        # assert isinstance(payload[0]["id_channel"], int)

        result = result[:5]
        if verbose:
            logging.info(pformat(result))

    def test_query_video_by_channel(self, verbose: bool = True, csv: bool = True):
        """ """

        # cest pas sorcier
        id_channel = "UCENv8pH4LkzvuSV_qHIcslg"

        result, _ = _query_videos_by_channel(id_channel=id_channel, days_max=360)

        result = result[:5]
        if verbose:
            logging.info(pformat(result))
