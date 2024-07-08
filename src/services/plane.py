from .models import Service, Student
from .get_request import get_request
from src.logger import warning

issue_states = {
    "80ea7b83-467a-40e6-bc89-2ee6bad2c4cb": "done",
    "0cba5ea3-e5c1-47be-bdf8-1142a2f44b40": "in progress",
    "febb8d6b-e80e-4ade-aedf-0883e3583bce": "todo",
    "48c89c98-0074-413a-afbe-0968b421fd5d": "cancelled",
    "614a4ab9-e51d-4427-b803-1677fc49bef5": "backlog"
}  # (state: representation)


class Plane(Service):
    def parse_student_activity(self, student: Student):
        if student.Plane_workspace is None:
            warning(f"Student '{student.name}' does not have Plane workspace.")
            return True

        projects = get_request(
            url=self.url + f"/api/v1/workspaces/{student.Plane_workspace}/projects/",
            headers={
                "x-api-key": self.token
            },
            params={}
        )  # get projects in workspace

        if projects is None:
            return False  # failed to connect

        if projects.status_code != 200:
            warning(f"Failed to find user's ({student.name}) workspace '{student.Plane_workspace}' on Plane!")
            return True

        projects = projects.json()["results"]

        for project in projects:
            issues = get_request(
                url=self.url + f"/api/v1/workspaces/{student.Plane_workspace}/projects/{project['id']}/issues/",
                headers={
                    "x-api-key": self.token
                }
            )  # get all issues in projects

            if issues.status_code != 200:
                warning(f"Plane error receiving information about student's '{student.name}'"
                        f" '{student.Plane_workspace}': '{issues.json()['detail']}' !")
                return True

            active_issues = []
            for issue in issues.json()["results"]:
                if issue_states[issue["state"]] == "in progress":
                    active_issues.append(issue["name"])  # save all issues 'in projects'

            active_issues = active_issues.sort()  # issues sorted by alphabetic orger
            student.active_tasks = active_issues

            return True
