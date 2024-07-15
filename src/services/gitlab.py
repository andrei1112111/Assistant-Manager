from __future__ import annotations

from src.config import config
from .base_service import BaseService
from .get_request import get_request
from src.db.entity import StudentDB, LogDB

import datetime
from pytz import timezone
import requests


class GitLab(BaseService):
    def fill_student_activity(self, student: StudentDB, log: LogDB):
        gitlab_username = student.logins.get("gitlab", None)

        if gitlab_username is None:
            raise Exception(f"Student '{student.name}' does not have Gitlab username.")

        # get user id
        student_id = get_request(
            url=self.url + f"/api/v4/users/",
            params={
                "username": gitlab_username
            },
            headers={
                "Authorization": f"Bearer {config.Gitlab.token}"
            }
        )
        if student_id is None:
            raise Exception(f'Failed to connect to "{self.url + f"/api/v4/users/"}".')

        if student_id.status_code == requests.codes.ok:
            student_id = student_id.json()[0]["id"]
        else:
            raise Exception(
                f"{student_id.content}" +
                f"({student_id.status_code},"
                f" {self.url + f'/api/v4/users/'} for {gitlab_username})"
            )

        yesterday_date = datetime.datetime.now(tz=timezone(str(config.timezone))) - datetime.timedelta(1)  # yesterday
        yesterday_date = yesterday_date.strftime("%Y-%m-%d")

        tomorrow_date = datetime.datetime.now(tz=timezone(str(config.timezone))) + datetime.timedelta(1)  # tomorrow
        tomorrow_date = tomorrow_date.strftime("%Y-%m-%d")  # like '2024-03-09'

        student_commits = get_request(  # get all commits by student.GitLab_username created today
            url=self.url + f"/api/v4/users/{student_id}/events",
            params={
                "action": "commit",
                "after": yesterday_date,
                "before": tomorrow_date,
            },
            headers={
                "Authorization": f"Bearer {config.Gitlab.token}"
            }
        )
        if student_commits is None:
            raise Exception(f'Failed to connect to "{self.url + f"/api/v4/users/{student_id}/events"}".')

        if student_commits.status_code == requests.codes.ok:
            log.count_gitlab_commits = len(student_commits.json())  # set commits count
        else:
            raise Exception(
                f"{student_commits.content}" +
                f"({student_commits.status_code},"
                f" {self.url + f'/api/v4/users/{student_id}/events'} for {gitlab_username})"
            )
