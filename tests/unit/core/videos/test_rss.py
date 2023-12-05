import pytest

import pandas as pd
import logging

from src.core.videos.rss import build_rss, _extract_rss

from pandarallel import pandarallel


class TestRSS:
    """ """

    def test_extract_rss(self):
        """ """

        id_channel = "UCFqV9b9ji8yIMw3GyNlueuA"
        results = _extract_rss(id_channel)

        logging.info(results)

        assert isinstance(results, list)
        assert results
        assert isinstance(results[0], dict)

    def test_build_rss(self):
        """ " """

        df = pd.DataFrame(
            {
                "id_channel": [
                    "UCFqV9b9ji8yIMw3GyNlueuA",
                    "UC8ggH3zU61XO0nMskSQwZdA",
                ]
            }
        )

        pandarallel.initialize(nb_workers=1)

        df = build_rss(
            df,
            video_detail=True,
            categ_1=True,
            parrallel=True,
        )

        cols = ["title", "id_categ_1"]
        df = df.loc[:, cols]
        # df.to_csv("tmp.csv", index=False)
