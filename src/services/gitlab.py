from .models import Service
from .models.service_model import Student
from .get_request import get_request
from src.logger import logger
import datetime
from pytz import timezone
from src.config import config


class GitLab(Service):
    def parse_student_activity(self, student: Student) -> bool:
        if student.GitLab_username is None:
            logger.warning(f"Student '{student.name}' does not have Gitlab username.")
            return True

        yesterday_date = datetime.datetime.now(tz=timezone(config.time.timezone)) - datetime.timedelta(1)  # yesterday
        yesterday_date = yesterday_date.strftime("%Y-%m-%d")

        tomorrow_date = datetime.datetime.now(tz=timezone(config.time.timezone)) + datetime.timedelta(1)  # tomorrow
        tomorrow_date = tomorrow_date.strftime("%Y-%m-%d")  # like '2024-03-09'

        student_commits = get_request(  # get all commits by student.GitLab_username created today
            url=self.url + f"/api/v4/users/{student.GitLab_username}/events",
            params={
                "action": "commit",
                "after": yesterday_date,
                "before": tomorrow_date
            },
            headers={}
        )

        if student_commits is None:
            return False  # failed to connect

        if student_commits.status_code == 200:  # 'OK' statis code
            student.commits_count = len(student_commits.json())  # set commits count
        else:
            logger.warning(f"For student '{student.name}' with Gitlab username '{student.GitLab_username}'"
                           f" an error has occurred: '{student_commits.json()['message']}'.")

        return True
