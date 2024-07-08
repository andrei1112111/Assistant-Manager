from .models import Service, Student
from .get_request import get_request
from src.logger import error, warning
import datetime


class Kimai(Service):
    def parse_student_activity(self, student: Student) -> bool:
        if student.Kimai_username is None:
            warning(f"Student '{student.name}' does not have Kimai username.")
            return True

        users = get_request(
            url=self.url + f"/api/users",
            headers={
                "Authorization": f"Bearer {self.token}",
            },
            params={
                "visible": "3"
            }
        )  # get all users [{user dict with "id"}]

        if users is None:
            return False  # failed to connect

        if users.status_code != 200:
            # logging the error message
            if "message" in users.json().keys():
                error(f"Kimai (get users) returns an error: '{users.json()['message']}' !")
            else:
                error(f"Kimai (get users) return NOTHING! Maybe this is an authorization error !")  # \
            return False  # failed to use api

        users = users.json()

        current_date = datetime.datetime.now()  # current date
        current_date = current_date.strftime("%Y-%m-%d")  # like '2024-03-09'

        # find kimai user_id's by student Kimai_username
        users_with_same_name = [
            user["username"] for user in users if user["username"] == student.Kimai_username
        ]

        if len(users_with_same_name) == 0:  # Kimai does not even know such a user
            warning(f"The user '{student.name}' is not registered in the Kimai"
                    f" or has a different username from the specified one! ")
            return True

        user_id = users_with_same_name[0]

        # get user timesheets
        timesheets = get_request(
            url=self.url + f"/api/timesheets", headers={
                "Authorization": f"Bearer {self.token}"
            }, params={
                "user": user_id,
                "begin": f"{current_date}T00:00:00",  # by server time
                "end": f"{current_date}T23:59:59"
            }
        )

        if timesheets.status_code != 200:
            warning(f"An error occurred while receiving the timesheets on Kimai: '{users['message']}'")
            return True

        student.worked_time = sum(
            [
                timesheet["duration"] for timesheet in timesheets.json()
            ]
        )

        return True
