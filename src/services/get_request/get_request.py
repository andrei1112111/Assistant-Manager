from __future__ import annotations

from requests.adapters import HTTPAdapter, Retry
from dataclasses import dataclass
import requests as rq

from .retry_config import RetryConfig


def get_request(
        url: str,
        params: dict,
        headers: dict,
        timeout_seconds: int = 1,
        retry_params: dataclass = RetryConfig(
            max_attempts=2,
            delay_seconds=1
        )
) -> rq.Response | None:
    """
    :return: None when failed to connect else response object
    """
    with rq.Session() as session:  # the official documentation of requests advises to do like that
        retries = Retry(
            total=retry_params.max_attempts,
            backoff_factor=retry_params.delay_seconds
        )
        # set max_retries for all http/https request
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))

        try:
            resp = session.get(
                url=url, params=params, headers=headers, timeout=timeout_seconds
            )
            return resp

        except rq.exceptions.ConnectionError:
            return
