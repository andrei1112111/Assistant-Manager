from .configure_logger import configure_logger
from logging import info, warning, critical, error

configure_logger()

__all__ = [
    "info",
    "warning",
    "critical",
    "error",
]
