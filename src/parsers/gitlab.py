from __future__ import annotations

from common.common import Student, trace, internet_on

from logging import info
import requests as rq
import datetime


@trace
def parse_commits(students: list[Student], host: str, token: str, secret: str) -> dict[str: int | None]:
    """
    Get commit count by gitlab api for list of students
    :param students: List of students
    :param host: server address
    :param token: token is not required
    :param secret: secret key is not required
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
            [student.git for student in students if student.git is not None],
            [parse_student(student.git, after_date, before_date, host) for student in students if student.git is not None]
        ) if c is not None
    }


def parse_student(student_git: str, after_date: str, before_date: str, host: str) -> int | None:
    """
    Get student commits count on gitlab between before_date and after_date
    :param student_git: Gitlab username
    :param after_date: yesterday date
    :param before_date: tomorrow date
    :param host: server address
    :return: commits count or None in case of a problem with getting data from api
    """
    if student_git is None:
        return
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
        info(f"Gitlab user '{student_git}' - {data.json()['message']}")  # logging the error message
