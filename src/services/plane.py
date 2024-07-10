from __future__ import annotations

from src.config import config
from .base_service import BaseService
from .get_request import get_request
from src.db.entity import StudentDB, LogDB

import datetime
from pytz import timezone

issue_states = {
    "80ea7b83-467a-40e6-bc89-2ee6bad2c4cb": "done",
    "0cba5ea3-e5c1-47be-bdf8-1142a2f44b40": "in progress",
    "febb8d6b-e80e-4ade-aedf-0883e3583bce": "todo",
    "48c89c98-0074-413a-afbe-0968b421fd5d": "cancelled",
    "614a4ab9-e51d-4427-b803-1677fc49bef5": "backlog"
}  # meaning of status codes


class Plane(BaseService):
    def fill_student_activity(self, student: StudentDB, log: LogDB) -> str | None:
        plane_workspace = student.logins.get("plane", None)

        if plane_workspace is None:
            return f"Student '{student.name}' does not have Plane workspace."

        projects = get_request(  # get projects in workspace
            url=self.url + f"/api/v1/workspaces/{plane_workspace}/projects/",
            headers={
                "x-api-key": self.token
            },
            params={}
        )

        if projects is None:
            return f'Failed to connect to "{self.url + f"/api/v1/workspaces/{plane_workspace}/projects/"}".'

        if projects.status_code != 200:
            return f"Failed to find user's '{student.name}' workspace '{plane_workspace}'."

        projects = projects.json()["results"]

        for project in projects:
            issues = get_request(  # get all issues in projects
                url=self.url + f"/api/v1/workspaces/{plane_workspace}/projects/{project['id']}/issues/",
                headers={
                    "x-api-key": self.token
                },
                params={}
            )

            if issues.status_code != 200:
                return f"For student '{student.name}': {issues.json()['detail']}'."

            active_issues = []
            for issue in issues.json()["results"]:
                if issue_states[issue["state"]] == "in progress":
                    active_issues.append(issue["name"])  # save all issues with status 'in progress'

            active_issues.sort()  # issues are sorted by alphabetic orger
            log.plane_tasks = ', '.join(active_issues)
