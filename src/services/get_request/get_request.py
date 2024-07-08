from __future__ import annotations

import requests as rq
from src.logger import error
from time import sleep


def get_request(url: str, params: dict, headers: dict) -> rq.Response | None:
    for i in range(5):
        try:
            result = rq.get(
                url=url, params=params, headers=headers, timeout=2
            )

            return result

        except rq.exceptions.ConnectionError as _:
            sleep(5)

            pass  # retry to connect

    error(f"Failed to connect to the server '{url}' !")
    return None
