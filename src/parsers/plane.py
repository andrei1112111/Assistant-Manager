from __future__ import annotations

from src.additional import Student, trace, internet_on

from logging import info
import requests as rq
from configparser import ConfigParser

config = ConfigParser()
config.read("config/settings.ini")

issue_states = {
    "80ea7b83-467a-40e6-bc89-2ee6bad2c4cb": "done",
    "0cba5ea3-e5c1-47be-bdf8-1142a2f44b40": "in progress",
    "febb8d6b-e80e-4ade-aedf-0883e3583bce": "todo",
    "48c89c98-0074-413a-afbe-0968b421fd5d": "cancelled",
    "614a4ab9-e51d-4427-b803-1677fc49bef5": "backlog"
}  # (state: representation)


@trace
def parse_active_tasks(students: list[Student]) -> dict[str: list[str]]:
    """
    Get active issues for students workspace
    :param students: student's workspace
    :return: active issues for every student workspace
    """
    if not internet_on(config['Services hosts']['plane']):
        return
    return {
        s: c for s, c in zip(
            [student.plane for student in students if student.plane is not None],
            [[j for j in parse_student(student.plane)] for student in students if student.plane is not None]
        )
    }


def parse_student(student_plane: str) -> list[str] | None:
    """
    Get active issues for current student workspace
    :param student_plane: student's workspace
    :return: list of active issues
    """
    if student_plane is None:
        return
    data = rq.get(
        config['Services hosts']['plane'] + f"/api/v1/workspaces/{student_plane}/projects/", headers={
            "x-api-key": config['API Tokens']['plane']
        }
    )  # get projects in workspace
    if data.status_code != rq.codes.ok:
        info(f"[INFO] Plane (get projects) user '{student_plane}' - {data.json()['detail']}")  # \
        # \ logging the error message
        return
    projects = data.json()["results"]  # get all projects in workspace
    for proj in projects:
        issues = rq.get(
            config['Services hosts']['plane'] + f"/api/v1/workspaces/{student_plane}/projects/{proj['id']}/issues/",
            headers={
                "x-api-key": config['API Tokens']['plane']
            }
        )  # get all issues in projects
        if issues.status_code != rq.codes.ok:
            info(f"[INFO] Plane (get issues) user '{student_plane}' - {issues.json()['detail']}")  # \
            # \ logging the error message
            return
        for issue in issues.json()["results"]:
            if issue_states[issue["state"]] == "in progress":
                yield issue["name"]  # return all issues 'in projects'
