from logging import basicConfig, INFO, StreamHandler
from sys import stdout


def configure_logger():
    basicConfig(
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[StreamHandler(stdout)],
        datefmt="%Y-%m-%d %H:%M:%S",
        level=INFO
    )
