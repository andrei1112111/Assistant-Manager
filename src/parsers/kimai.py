from __future__ import annotations

from common.common import Student, trace, internet_on

from logging import warning
import requests as rq
import datetime


@trace
def parse_active_hours(students: list[Student], host: str, token: str, secret: str) -> dict[str: int] | None:
    """
    Get total timesheets duration by kimai api for list of students
    :param students: List of students
    :param host: server address
    :param token: API kimai token
    :param secret: secret key is not required
    :return: total timesheets duration in minutes for every student
    """
    if not internet_on(host):
        return
    result = {}
    users = rq.get(
        host + f"/api/users", headers={
            "Authorization": f"Bearer {token}",
        }, params={
            "visible": "3"
        }
    )  # get all users [{user dict with "id"}]
    if users.status_code != rq.codes.ok:
        try:
            warning(f"Kimai (get users) - {users.json()['message']}")  # logging the error message
        except rq.exceptions.JSONDecodeError:
            warning(f"Kimai (get users) return NOTHING. Maybe this is an authorization error")  # \
            # \ logging the error message
        return
    users = users.json()
    """filter users by students"""
    studentnames = [student.kimai for student in students if student.kimai is not None]
    usernames = {user["id"]: user["username"] for user in users if user["username"] in studentnames}  # \
    # \ (student_id: student_username) contains only students
    """get timesheets sum for every student"""
    current_date = datetime.datetime.now()  # current date
    current_date = current_date.strftime("%Y-%m-%d")  # like '2024-03-09'
    for user in usernames.keys():
        timesheets = rq.get(
            host + f"/api/timesheets", headers={
                "Authorization": f"Bearer {token}"
            }, params={
                "user": user,
                "begin": f"{current_date}T00:00:00",  # by server time
                "end": f"{current_date}T23:59:59"
            }
        )  # get user timesheets
        if timesheets.status_code != rq.codes.ok:
            warning(f"Kimai (get timesheets) - {users['message']}")  # logging the error message
            return
        result[usernames[user]] = sum([timesheet["duration"] for timesheet in timesheets.json()])  # \
        # \ result[username] = sum of timesheet durations
    return result
