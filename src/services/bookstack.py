from __future__ import annotations

from src.db.entity import StudentDB, LogDB
from .base_service import BaseService
from .get_request import get_request
from src.config import config
from pytz import timezone
import datetime


class BookStack(BaseService):
    def fill_student_activity(self, student: StudentDB, log: LogDB) -> str | None:
        bookstack_username = student.logins.get("bookstack", None)

        if bookstack_username is None:
            return f"Student '{student.name}' doesn't have Bookstack username."

        user_id = get_request(  # get all users with name like student.Bookstack_username
            url=self.url + "/api/users",
            headers={
                "Authorization": f"Token {self.token}:{self.secret}"
            },
            params={
                "filter[name:like]": bookstack_username
            }
        )
        if user_id is None:
            return f'Failed to connect to "{self.url + "/api/users"}".'

        if user_id.json()["total"] == 0:  # such users are not founded
            return (f"The user '{student.name}' is not registered in the Bookstack"
                    f" or has a different username from the specified one.")

        current_date = datetime.datetime.now(tz=timezone(str(config.timezone)))  # current date
        current_date = current_date.strftime("%Y-%m-%d")  # like '2024-03-09'

        audit = get_request(  # get changes-log for student.Bookstack_username-id created today
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
            return f'Failed to connect to "{self.url + "/api/audit-log"}".'

        log.count_bookstack_changes = audit.json()["total"]  # set number of changes
