from typing import List

from configparser import ConfigParser
from logging import warning, critical, debug
from urllib import request
import pytz
import sys
import os

CORRECT_CONFIG = {
    "Time": ("timezone", "schedule_time"),
    "Services hosts": ("plane", "kimai", "gitlab", "bookstack"),
    "API Tokens": ("plane_token", "kimai_token"),
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
        # debug(f'TRACE: calling {func.__name__}() '
        #       f'with {args}, {kwargs}')

        original_result = func(*args, **kwargs)

        debug(f'TRACE: {func.__name__}() '
              f'returned {original_result!r}')
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
        warning(f"Connection to {host} failed!")
        return False


def parse_db() -> List[Student]:
    # students for testing
    students = [
        Student(
            "root",
            "None",
            "Admin",
            "admin"
        ),
        Student(
            "testtest",  # gitlab nickname
            "testingworkspace",  # ? plane workspace name
            None,  # bookstack username
            "TestUser1"  # kimai username
        ),
        Student(
            "not_existing_user",
            None,
            None,
            "not exist"
        ),
        Student(
            None,
            None,
            None,
            None
        ),
    ]
    # -
    return students


def check_config(path: str) -> None:
    """
    Checks if the configuration file is written correctly
    :param path: Path to the configuration files
    """
    """check structure"""
    config = ConfigParser()
    config.read(path)
    if not os.path.exists(path):
        critical(f"Failed to find '{path}' in configuration file")
        sys.exit(6)
    for section in CORRECT_CONFIG.keys():
        if section not in config.sections():
            critical(f"Missing section '{section}' in configuration file")
            sys.exit(6)
        for option in CORRECT_CONFIG[section]:
            if option not in config.options(section):
                critical(f"Missing option '{option}' in section '{section}' in configuration file")
                sys.exit(6)
    """check time options"""
    try:
        pytz.timezone(config['Time']['timezone'])
    except pytz.exceptions.UnknownTimeZoneError:
        if not isinstance(config['Time']['timezone'], pytz.BaseTzInfo):
            critical(f"Incorrect timezone '{config['Time']['timezone']}' in configuration file")
            sys.exit(6)
    if len(str(config['Time']['schedule_time'])) != 5 or not all([
        config['Time']['schedule_time'][0].isdigit(),
        config['Time']['schedule_time'][1].isdigit(),
        config['Time']['schedule_time'][2] == ':',
        config['Time']['schedule_time'][3].isdigit(),
        config['Time']['schedule_time'][4].isdigit()
    ]):
        critical(f"Incorrect schedule_time format '{config['Time']['schedule_time']}' in configuration file")
        sys.exit(6)
    return  # config is correct


def check_env_vars():
    """
    Checks if the environment variables is set correctly
    """
    """check structure"""
    for variable in ["TIMEZONE", "schedule_time",
                     "PLANE", "KIMAI", "BOOKSTACK", "GITLAB",
                     "PLANE_TOKEN", "KIMAI_TOKEN", "BOOKSTACK_TOKEN", "BOOKSTACK_SECRET"
                     ]:
        if os.environ.get(variable) is None:
            critical(f"Missing environment variable '{variable}'")
            sys.exit(6)
    timezone = os.environ.get("TIMEZONE")
    schedule_time = os.environ.get("schedule_time")
    """check time options"""
    try:
        pytz.timezone(timezone)
    except pytz.exceptions.UnknownTimeZoneError:
        if not isinstance(timezone, pytz.BaseTzInfo):
            critical(f"Incorrect timezone '{timezone}' in configuration file")
            sys.exit(6)
    if len(str(schedule_time)) != 5 or not all([
        schedule_time[0].isdigit(),
        schedule_time[1].isdigit(),
        schedule_time[2] == ':',
        schedule_time[3].isdigit(),
        schedule_time[4].isdigit()
    ]):
        critical(f"Incorrect schedule_time format '{schedule_time}' in configuration file")
        sys.exit(6)
    return  # environment variables are correct
