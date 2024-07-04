from __future__ import annotations

import requests.exceptions

from src.additional import Student, trace, internet_on

from logging import info
import requests as rq
from configparser import ConfigParser
import datetime

config = ConfigParser()
config.read("config/settings.ini")


@trace
def parse_active_hours(students: list[Student]) -> dict[str: int] | None:
    """
    .?.
    :param students: List of students
    :return: total timesheets duration in minutes for every student
    """
    if not internet_on(config['Services hosts']['kimai']):
        return
    result = {}
    users = rq.get(
        config['Services hosts']['kimai'] + f"/api/users", headers={
            "Authorization": f"Bearer {config['API Tokens']['kimai']}",
        }, params={
            "visible": "3"
        }
    )  # get all users [{user dict with "id"}]
    if users.status_code != rq.codes.ok:
        try:
            info(f"[WARNING] kimai (get users) - {users.json()['message']}")  # logging the error message
        except requests.exceptions.JSONDecodeError:
            info(f"[WARNING] kimai (get users) return NOTHING. Maybe this is an authorization error")  # \
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
            config['Services hosts']['kimai'] + f"/api/timesheets", headers={
                "Authorization": f"Bearer {config['API Tokens']['kimai']}"
            }, params={
                "user": user,
                "begin": f"{current_date}T00:00:00",  # by server time
                "end": f"{current_date}T23:59:59"
            }
        )  # get user timesheets
        if timesheets.status_code != rq.codes.ok:
            info(f"[WARNING] kimai (get timesheets) - {users['message']}")  # logging the error message
            return
        result[usernames[user]] = sum([timesheet["duration"] for timesheet in timesheets.json()])  # \
        # \ result[username] = sum of timesheet durations
    return result
