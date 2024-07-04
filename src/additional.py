from configparser import ConfigParser
from logging import warning, critical
from urllib import request
from os.path import exists

import pytz

import sys

CORRECT_CONFIG = {
    "Time": ("timezone", "wakeup time"),
    "Services hosts": ("plane", "kimai", "gitlab", "bookstack"),
    "API Tokens": ("plane", "kimai"),
}


class Student:
    """
    Information about student
    """

    def __init__(self, gitlab, plane, bookstack, kimai):
        self.git: str = gitlab
        self.plane: str = plane
        self.bookstack: str = bookstack
        self.kimai: str = kimai


def trace(func):
    """
    tracer for debug
    """

    def wrapper(*args, **kwargs):
        print(f'TRACE: calling {func.__name__}() '
              f'with {args}, {kwargs}')

        original_result = func(*args, **kwargs)

        print(f'TRACE: {func.__name__}() '
              f'returned {original_result!r}')
        print()
        return original_result

    return wrapper


def internet_on(host: str, timeout: int = 1) -> bool:
    """
    Check there is connection to website by address and timeout
    :param timeout: connection timeout
    :param host: website address
    :return: True if there is connection to website. False otherwise
    """
    try:
        request.urlopen(host, timeout=timeout)
        return True
    except request.URLError as _:
        warning(f"[WARNING] Connection to {host} failed!")
        return False


def check_config(path: str) -> None:
    """
    Checks if the configuration file is written correctly
    :param path: Path to the configuration files
    """
    """check structure"""
    config = ConfigParser()
    config.read(path)
    if exists(path) is not True:
        critical(f"[CRITICAL] failed to find '{path}' in configuration file")
        sys.exit(6)
    for section in CORRECT_CONFIG.keys():
        if section not in config.sections():
            critical(f"[CRITICAL] missing section '{section}' in configuration file")
            sys.exit(6)
        for option in CORRECT_CONFIG[section]:
            if option not in config.options(section):
                critical(f"[CRITICAL] missing option '{option}' in section '{section}' in configuration file")
                sys.exit(6)
    """check time options"""
    try:
        pytz.timezone(config['Time']['timezone'])
    except pytz.exceptions.UnknownTimeZoneError:
        if not isinstance(config['Time']['wakeup time'], pytz.BaseTzInfo):
            critical(f"[CRITICAL] incorrect timezone '{config['Time']['timezone']}' in configuration file")
            sys.exit(6)
    if len(str(config['Time']['wakeup time'])) != 5 or not all([
        config['Time']['wakeup time'][0].isdigit(),
        config['Time']['wakeup time'][1].isdigit(),
        config['Time']['wakeup time'][2] == ':',
        config['Time']['wakeup time'][3].isdigit(),
        config['Time']['wakeup time'][4].isdigit()
    ]):
        critical(f"[CRITICAL] incorrect wakeup time format '{config['Time']['wakeup time']}' in configuration file")
        sys.exit(6)
    return  # all OK
