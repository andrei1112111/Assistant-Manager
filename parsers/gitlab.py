from __future__ import annotations

from objects import Student, trace

from logging import info, warning
from urllib import request
import requests as rq
import datetime


def internet_on(host):
    try:
        request.urlopen(host, timeout=1)
        return True
    except request.URLError as _:
        warning(f"WARNING: Failed to connect to {host}")
        return False


@trace
def parse_commits(peoples: list[Student], host: str) -> dict[str: int | None]:
    """
    Get commit count by gitlab api for list of students
    :param peoples: List of students
    :param host: service url
    :return: dictionary of the format: 'student_username: number_of_commits_for_the_current_date'
    """
    if not internet_on(host):
        return
    after_date = datetime.datetime.now() - datetime.timedelta(1)  # yesterday
    before_date = datetime.datetime.now() + datetime.timedelta(1)  # tomorrow
    after_date = after_date.strftime("%Y-%m-%d")
    before_date = before_date.strftime("%Y-%m-%d")  # like '2024-03-09'
    return {
        s: c for s, c in zip(
            [i.git for i in peoples],
            [parse_student(i.git, after_date, before_date, host) for i in peoples]
        )
    }


def parse_student(student_git: str, after_date: str, before_date: str, host: str) -> int | None:
    """
    Get student commits count on gitlab for the current date
    :param student_git: Gitlab username
    :param after_date: yesterday date
    :param before_date: tomorrow date
    :param host: service url
    :return: commits count or None in case of a problem with getting data from api
    """
    data = rq.get(
        host + f"/api/v4/users/{student_git}/events", params={
            "action": "commit",
            "after": after_date,
            "before": before_date
        }
    )
    if data.status_code == rq.codes.ok:
        return len(data.json())
    else:
        info(f"INFO: Gitlab {student_git} - {data.json()['message']}")  # logging the error message
