from __future__ import annotations

from src.config import config
from .base_service import BaseService
from .get_request import get_request
from src.db.entity import StudentDB, LogDB

import datetime
from pytz import timezone
import requests


class Kimai(BaseService):
    def fill_student_activity(self, student: StudentDB, log: LogDB) -> str | None:
        kimai_username = student.logins.get("gitlab", None)

        if kimai_username is None:
            return f"Student '{student.name}' does not have Kimai username."

        users = get_request(  # get all users
            url=self.url + f"/api/users",
            headers={
                "Authorization": f"Bearer {self.token}",
            },
            params={
                "visible": "3"
            }
        )

        if users is None:
            return f'Failed to connect to "{self.url + f"/api/users"}".'

        if users.status_code != requests.codes.ok:
            if "message" in users.json().keys():
                return users.json()['message']
            else:
                return "Kimai return nothing when users are requested. Maybe this is an authorization error."

        users = users.json()

        # get all ids of usernames with the same name
        users_with_same_name = [
            user["username"] for user in users if user["username"] == kimai_username
        ]

        if len(users_with_same_name) == 0:  # we not find users with name = kimai_username
            return f"The user '{student.name}' is not registered in the Kimai."

        user_id = users_with_same_name[0]  # there is probably only one such user

        current_date = datetime.datetime.now(tz=timezone(str(config.timezone)))  # current date
        current_date = current_date.strftime("%Y-%m-%d")  # like '2024-03-09'

        # get user timesheets
        timesheets = get_request(
            url=self.url + f"/api/timesheets", headers={
                "Authorization": f"Bearer {self.token}"
            }, params={
                "user": user_id,
                "begin": f"{current_date}T00:00:00",
                "end": f"{current_date}T23:59:59"
            }
        )

        if timesheets.status_code != requests.codes.ok:
            if "message" in timesheets.json().keys():
                return f"{timesheets.json()['message']}"
            else:
                return f"Kimai api return nothing when timesheets are requested."

        log.count_kimai_hours = round(
            sum(  # sum duration of timesheets
                [
                    timesheet["duration"] for timesheet in timesheets.json()
                ]
            ) / 60,  # in hours
            3  # rounded to three decimal places (for ex. 61 minutes = 1.017 hours)
        )
