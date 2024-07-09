from .models import Service, Student
from .get_request import get_request
from src.logger import logger
import datetime
from pytz import timezone
from src.config import config


class Kimai(Service):
    def parse_student_activity(self, student: Student) -> bool:
        if student.Kimai_username is None:
            logger.warning(f"Student '{student.name}' does not have Kimai username.")
            return True

        users = get_request(  # get all users
            url=self.url + f"/api/users",
            headers={
                "Authorization": f"Bearer {self.token}",
            },
            params={
                "visible": "3"
            }
        )

        if users is None:
            return False  # failed to connect

        if users.status_code != 200:
            if "message" in users.json().keys():
                logger.error(f"Kimai (when get users) returns an error: '{users.json()['message']}' !")
            else:
                logger.error(f"Kimai (when get users) return NOTHING! Maybe this is an authorization error !")
            return False  # failed to use api

        users = users.json()

        current_date = datetime.datetime.now(tz=timezone(config.time.timezone))  # current date
        current_date = current_date.strftime("%Y-%m-%d")  # like '2024-03-09'

        # find kimai user_id's by student Kimai_username
        users_with_same_name = [
            user["username"] for user in users if user["username"] == student.Kimai_username
        ]

        if len(users_with_same_name) == 0:  # Kimai does not even know such a user
            logger.warning(f"The user '{student.name}' is not registered in the Kimai"
                           f" or has a different username from the specified one! ")
            return True

        user_id = users_with_same_name[0]  # there is probably only one such user

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
            if "message" in timesheets.json().keys():
                logger.warning(f"An error occurred while receiving"
                               f" the timesheets on Kimai: '{timesheets.json()['message']}'")
            else:
                logger.warning(f"Kimai api return's nothing when timesheets are requested.")
            return True

        student.worked_time = sum(  # set sum of timesheets duration
            [
                timesheet["duration"] for timesheet in timesheets.json()
            ]
        )

        return True
