from __future__ import annotations

import requests as rq
from src.logger import logger
from time import sleep


def get_request(url: str,
                params: dict,
                headers: dict,
                retry_count: int = 5,
                timeout: int = 2,
                frequency: int = 5) -> rq.Response | None:
    """
    :param url:
    :param params:
    :param headers:
    :param retry_count: retry_count: how many times will the request be attempted if the server is not responding
    :param timeout: timeout for request in seconds
    :param frequency: the frequency with which requests will be sent if the server is not responding
    :return:
    """
    for i in range(retry_count):
        try:
            result = rq.get(
                url=url, params=params, headers=headers, timeout=timeout
            )
            return result

        except rq.exceptions.ConnectionError as _:
            sleep(frequency)
            pass  # retry to connect

    logger.error(f"Failed to connect to the server '{url}' !")
    return None
