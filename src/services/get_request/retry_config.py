from dataclasses import dataclass


@dataclass
class RetryConfig:
    max_attempts: int
    delay: int


def_retry_conf = RetryConfig(
    max_attempts=5,
    delay=2
)
