import os
import logging

from dotenv import load_dotenv, dotenv_values


def get_params(MODE: str = "dev") -> dict:
    """set params from .env file or from os.environ

    Opt Args:
        MODE : str: mode of the api in [dev, main]. Defaults to "dev".

    Returns:
        dict: params of the api"""

    # if mode is not dev or main, then it must be defined in os.environ
    if MODE not in ["dev", "main"]:
        api_mode = os.getenv("MODE")
        if not api_mode:
            raise ValueError("MODE is not defined")

    # load .env file if needed
    try:
        if MODE == "dev":
            _params = dotenv_values(".env/.env.dev")
        elif MODE == "main":
            _params = dotenv_values(".env/.env.main")
    except Exception as e:
        logging.error(e)
        _params = {}

    # set params from os.environ as default
    _default_params = {
        "API_TOKEN": os.getenv("API_TOKEN", None),
        "API_HOST": os.getenv("API_HOST", None),
        "API_PORT": os.getenv("API_PORT", None),
        "API_MODE": os.getenv("API_MODE", None),
        "MYSQL_ROOT_PASSWORD": os.getenv("MYSQL_ROOT_PASSWORD", None),
        "MYSQL_DATABASE": os.getenv("MYSQL_DATABASE", None),
        "MYSQL_PASSWORD": os.getenv("MYSQL_PASSWORD", None),
        "MYSQL_HOST": os.getenv("MYSQL_HOST", None),
        "MYSQL_PORT": os.getenv("MYSQL_PORT", None),
        "PMA_HOST": os.getenv("PMA_HOST", None),
        "MYSQL_MODE": os.getenv("MYSQL_MODE", None),
    }

    # if not in dotenv load from os.environ
    params = {}
    for key, value in _default_params.items():
        params[key] = _params.get(key, value)

    # if null raise error
    if not [i for i in params.values() if i]:
        raise ValueError(f"No params defined : {params}")

    return params
