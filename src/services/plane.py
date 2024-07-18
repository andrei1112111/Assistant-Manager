from __future__ import annotations

from .base_service import BaseService
from .get_request import get_request
from src.db.entity import StudentDB, LogDB

import requests
import json
from os.path import exists


class Plane(BaseService):
    def fill_student_activity(self, student: StudentDB, log: LogDB):
        plane_data = student.logins.get("plane", None)

        if plane_data is None or len(plane_data.split("|")) != 2:
            raise Exception(f"Student '{student.name}' does not have Plane workspace or email.")

        plane_workspace, plane_email = plane_data.split("|")

        if not exists(self.token):
            raise Exception(f"Won't find plane tokens file {self.token}")

        with open(self.token, "r") as file:
            tokens = json.load(file)

        plane_workspace_token = tokens.get(plane_workspace, None)

        if plane_workspace_token is None:
            raise Exception(f"Plane workspace token for '{plane_workspace}' not exist in tokens file '{self.token}'.")

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
            raise Exception(f"Failed to find user's '{student.name}' workspace '{plane_workspace}'.")

        projects = projects.json()["results"]

        for project in projects:
            issues = get_request(  # get all issues in projects
                url=self.url + f"/api/v1/workspaces/{plane_workspace}/projects/{project['id']}/issues/",
                headers={
                    "x-api-key": plane_workspace_token
                },
                params={"expand": "assignees,state",
                        "fields": "assignees,state,name", }
            )

            if projects is None:
                raise ConnectionError(
                    f'Failed to connect to'
                    f' self.url + f"/api/v1/workspaces/{plane_workspace}/projects/{project["id"]}/issues/".'
                )

            if issues.status_code != requests.codes.ok:
                raise Exception(f"For student '{student.name}': {issues.json()['detail']}'.")

            active_issues = []
            for issue in issues.json()["results"]:
                if issue["state"]["group"] == "started" and \
                        plane_email in [i["email"] for i in issue["assignees"]]:
                    active_issues.append(issue["name"])  # save all issues with status 'in progress'

            active_issues.sort()  # issues are sorted by alphabetic orger
            log.plane_tasks = ', '.join(active_issues)
