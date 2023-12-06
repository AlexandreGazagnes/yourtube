import pytest

import pandas as pd
import logging

from src.core.videos.rss import _scrap_one, _scrap_list, _update_list

from pandarallel import pandarallel


class TestRSS:
    """ """

    def test_scrap_one_raw(self):
        """ """

        id_channel = "UCFqV9b9ji8yIMw3GyNlueuA"
        results = _scrap_one(id_channel, clean=False)

        logging.info(results)

        assert isinstance(results, list)
        assert results
        assert isinstance(results[0], dict)

        df = pd.DataFrame(results)
        df = df.astype(str)
        df.to_csv("./tmp/test_scrap_one_raw.csv", index=False)

    def test_scrap_one_clean(self):
        """ """

        id_channel = "UCFqV9b9ji8yIMw3GyNlueuA"
        results = _scrap_one(id_channel, clean=True)

        logging.info(results)

        assert isinstance(results, list)
        assert results
        assert isinstance(results[0], dict)

        pd.DataFrame(results).to_csv("./tmp/test_scrap_one_clean.csv", index=False)

    def test_scrap_list(self):
        """ " """

        channel_list = [
            "UCFqV9b9ji8yIMw3GyNlueuA",
            "UC8ggH3zU61XO0nMskSQwZdA",
        ]

        rss_list = _scrap_list(channel_list, parallel=True)
        assert isinstance(rss_list, list)
        assert rss_list
        assert isinstance(rss_list[0], dict)

        pd.DataFrame(rss_list).to_csv("./tmp/test_rss_list.csv", index=False)

    def test_update_list_details(self):
        """ """

        channel_list = [
            "UCFqV9b9ji8yIMw3GyNlueuA",
            "UC8ggH3zU61XO0nMskSQwZdA",
        ]

        rss_list = _scrap_list(channel_list, parallel=True)

        updated_rss_list_details = _update_list(
            rss_list, detail=True, categ_1=False, parallel=True
        )

        assert isinstance(updated_rss_list_details, list)
        assert updated_rss_list_details
        assert isinstance(updated_rss_list_details[0], dict)

        pd.DataFrame(updated_rss_list_details).to_csv(
            "./tmp/updated_rss_list_details.csv", index=False
        )

    def test_update_list_categ1(self):
        """ """

        channel_list = [
            "UCFqV9b9ji8yIMw3GyNlueuA",
            "UC8ggH3zU61XO0nMskSQwZdA",
        ]

        rss_list = _scrap_list(channel_list, parallel=True)

        updated_rss_list_categ1 = _update_list(
            rss_list, detail=False, categ_1=True, parallel=True
        )

        assert isinstance(updated_rss_list_categ1, list)
        assert updated_rss_list_categ1
        assert isinstance(updated_rss_list_categ1[0], dict)

        pd.DataFrame(updated_rss_list_categ1).to_csv(
            "./tmp/updated_rss_list_categ1.csv", index=False
        )

    def test_update_list_both(self):
        """ """

        channel_list = [
            "UCFqV9b9ji8yIMw3GyNlueuA",
            "UC8ggH3zU61XO0nMskSQwZdA",
        ]

        rss_list = _scrap_list(channel_list, parallel=True)

        updated_rss_list_both = _update_list(
            rss_list, detail=True, categ_1=True, parallel=True
        )

        assert isinstance(updated_rss_list_both, list)
        assert updated_rss_list_both
        assert isinstance(updated_rss_list_both[0], dict)

        pd.DataFrame(updated_rss_list_both).to_csv(
            "./tmp/updated_rss_list_both.csv", index=False
        )
