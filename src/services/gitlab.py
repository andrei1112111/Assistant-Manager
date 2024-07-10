from __future__ import annotations

from src.config import config
from .base_service import BaseService
from .get_request import get_request
from src.db.entity import StudentDB, LogDB

import datetime
from pytz import timezone


class GitLab(BaseService):
    def fill_student_activity(self, student: StudentDB, log: LogDB) -> str | None:
        gitlab_username = student.logins.get("gitlab", None)

        if gitlab_username is None:
            return f"Student '{student.name}' does not have Gitlab username."

        yesterday_date = datetime.datetime.now(tz=timezone(config.time.timezone)) - datetime.timedelta(1)  # yesterday
        yesterday_date = yesterday_date.strftime("%Y-%m-%d")

        tomorrow_date = datetime.datetime.now(tz=timezone(config.time.timezone)) + datetime.timedelta(1)  # tomorrow
        tomorrow_date = tomorrow_date.strftime("%Y-%m-%d")  # like '2024-03-09'

        student_commits = get_request(  # get all commits by student.GitLab_username created today
            url=self.url + f"/api/v4/users/{gitlab_username}/events",
            params={
                "action": "commit",
                "after": yesterday_date,
                "before": tomorrow_date
            },
            headers={}
        )
        if student_commits is None:
            return f'Failed to connect to "{self.url + f"/api/v4/users/{gitlab_username}/events"}".'

        if student_commits.status_code == 200:  # 'OK' statis code
            log.count_gitlab_commits = len(student_commits.json())  # set commits count
        else:
            return student_commits.json()['message']
