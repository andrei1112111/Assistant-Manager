from __future__ import annotations

import requests as rq
from src.logger import logger
from time import sleep
from dataclasses import dataclass
from .retry_config import def_retry_conf


def get_request(url: str,
                params: dict,
                headers: dict,
                timeout: int = 2,
                retry_params: dataclass = def_retry_conf) -> rq.Response | None:
    attempts = 0

    while attempts < retry_params.max_attempts:
        try:
            result = rq.get(
                url=url, params=params, headers=headers, timeout=timeout
            )

            return result
        except rq.exceptions.ConnectionError as _:
            attempts += 1
            sleep(retry_params.delay)

    logger.error(f"Failed to connect to '{url}'.")
    return None
