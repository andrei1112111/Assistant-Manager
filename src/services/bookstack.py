from .models import Service
from .models.service_model import Student
from .get_request import get_request
from src.logger import warning
import datetime


class BookStack(Service):
    def parse_student_activity(self, student: Student) -> bool:
        if student.Bookstack_username is None:
            warning(f"Student '{student.name}' does not have Bookstack username.")
            return True

        current_date = datetime.datetime.now()  # current date
        current_date = current_date.strftime("%Y-%m-%d")  # like '2024-03-09'

        user_id = get_request(
            url=self.url + "/api/users",
            headers={
                "Authorization": f"Token {self.token}:{self.secret}"
            },
            params={
                "filter[name:like]": student.Bookstack_username
            }
        )

        if user_id is None:
            return False  # failed to connect

        if user_id.json()["total"] == 0:
            warning(f"The user '{student.name}' is not registered in the Bookstack"
                    f" or has a different username from the specified one! ")
            return True

        audit = get_request(
            url=self.url + "/api/audit-log",
            headers={
                "Authorization": f"Token {self.token}:{self.secret}"
            },
            params={
                "filter[created_at:gt]": current_date,
                "filter[user:eq]": user_id.json()["data"][0]["id"]
            }
        )

        if audit is None:
            return False  # failed to connect

        student.bookstack_changes = audit.json()["total"]  # number of changes

        return True
