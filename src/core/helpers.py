import logging

import requests

# from bs4 import BeautifulSoup


def _manage_response(url, label="label"):
    """manage the response of a request"""

    try:
        response = requests.get(url)
        if not response.ok:
            logging.error(
                f"requests {label} not good code- {response.status_code} - {url}"
            )
            return ""

    except Exception as e:
        logging.error(f"requests jsut fail for {label}- {e} - {url}")
        return ""

    return response
