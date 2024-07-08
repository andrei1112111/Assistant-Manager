from .models import Service
from .models.service_model import Student
from .get_request import get_request
from src.logger import warning
import datetime


class GitLab(Service):
    def parse_student_activity(self, student: Student) -> bool:
        if student.GitLab_username is None:
            warning(f"Student '{student.name}' does not have Gitlab username.")
            return True

        after_date = datetime.datetime.now() - datetime.timedelta(1)  # yesterday
        before_date = datetime.datetime.now() + datetime.timedelta(1)  # tomorrow
        after_date = after_date.strftime("%Y-%m-%d")
        before_date = before_date.strftime("%Y-%m-%d")  # like '2024-03-09'

        student_commits = get_request(
            url=self.url + f"/api/v4/users/{student.GitLab_username}/events",
            params={
                "action": "commit",
                "after": after_date,
                "before": before_date
            },
            headers={}
        )

        if student_commits is None:
            return False  # failed to connect

        if student_commits.status_code == 200:  # 'OK' statis code
            student.commits_count = len(student_commits.json())  # write commits count
        else:
            warning(f"For Gitlab user '{student.GitLab_username}' an error has occurred:"
                    f" '{student_commits.json()['message']}'.")  # logging the error message

        return True
