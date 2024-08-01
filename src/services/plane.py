from __future__ import annotations

from .base_service import BaseService
from .get_request import get_request
from src.db.entity import StudentDB, ActivityLogDB

from src.db.repository import plane_tokens_list_repository

import requests


class Plane(BaseService):
    def fill_student_activity(self, student: StudentDB, log: ActivityLogDB):
        log.plane_tasks = ""
        plane_workspace = student.logins.get("plane_workspace", None)
        plane_email = student.logins.get("email", None)

        if (plane_workspace is None) or (plane_email is None):
            raise Exception(f"Student '{student.name} {student.surname}' doesnt have plane workspace or email.")

        plane_workspace = plane_workspace.strip()
        plane_email = plane_email.strip()

        plane_workspace_token = plane_tokens_list_repository.get_token_by_workspace(plane_workspace)

        if plane_workspace_token is None:
            raise Exception(f"Plane workspace token for '{plane_workspace}' not exist in tokens table.")

        plane_workspace_token = plane_workspace_token.strip()

        projects = get_request(  # get projects in workspace
            url=self.url + f"/api/v1/workspaces/{plane_workspace}/projects/",
            headers={
                "x-api-key": plane_workspace_token
            },
            params={}
        )

        if projects is None:
            raise ConnectionError(f'Failed to connect to'
                                  f' "{self.url + f"/api/v1/workspaces/{plane_workspace}/projects/"}".')

        if projects.status_code != requests.codes.ok:
            raise Exception(f"Failed to find user's '{student.name} {student.surname}' workspace '{plane_workspace}'.")

        projects = projects.json()["results"]

        active_issues = []
        for project in projects:
            issues = get_request(  # get all issues in projects
                url=self.url + f"/api/v1/workspaces/{plane_workspace}/projects/{project['id']}/issues/",
                headers={
                    "x-api-key": plane_workspace_token
                },
                params={"expand": "assignees,state",
                        "fields": "assignees,state,name", }
            )

            if issues is None:
                raise ConnectionError(
                    f'Failed to connect to'
                    f' self.url + f"/api/v1/workspaces/{plane_workspace}/projects/{project["id"]}/issues/".'
                )

            if issues.status_code != requests.codes.ok:
                raise Exception(f"For student '{student.name} {student.surname}': {issues.json()['detail']}'.")

            for issue in issues.json()["results"]:
                if issue["state"]["group"] == "started" and \
                        plane_email in [i["email"] for i in issue["assignees"]]:
                    active_issues.append(issue["name"])  # save all issues with status 'in progress'

        active_issues.sort()  # issues are sorted by alphabetic orger
        log.plane_tasks = ', '.join(active_issues)
