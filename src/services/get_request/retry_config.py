from dataclasses import dataclass


@dataclass
class RetryConfig:
    max_attempts: int
    delay_seconds: int
