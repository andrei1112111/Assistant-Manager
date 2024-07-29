from __future__ import annotations

from src.db.entity import StudentDB, ActivityLogDB
from .base_service import BaseService
from .get_request import get_request
from src.config import config
from pytz import timezone
import datetime
import requests


class BookStack(BaseService):
    def fill_student_activity(self, student: StudentDB, log: ActivityLogDB):
        bookstack_username = student.logins.get("bookstack", None)

        if bookstack_username is None:
            raise Exception(f"Student '{student.name} {student.surname}' doesn't have Bookstack username.")

        bookstack_username = bookstack_username.strip()

        user_id = get_request(  # get all users with name like a student.Bookstack_username
            url=self.url + "/api/users",
            headers={
                "Authorization": f"Token {self.token}:{self.secret}"
            },
            params={
                "filter[name:like]": bookstack_username
            }
        )
        if user_id is None:
            raise ConnectionError(f'Failed to connect to "{self.url + "/api/users"}".')

        if user_id.status_code != requests.codes.ok:
            raise Exception(f'Failed to get by api "{self.url + "/api/users"}" with status code {user_id.status_code}.')

        if user_id.json()["total"] == 0:  # such users are not founded
            raise Exception(f"The user '{student.name}' is not registered in the Bookstack"
                            f" or has a different username from the specified one.")

        current_date = datetime.datetime.now(tz=timezone(str(config.timezone)))  # current date
        current_date = current_date.strftime("%Y-%m-%d")  # like '2024-03-09'

        audit = get_request(  # get changes-log for a student.Bookstack_username-id created today
            url=self.url + "/api/pages",
            headers={
                "Authorization": f"Token {self.token}:{self.secret}"
            },
            params={
                "filter[updated_at:gt]": current_date,
                "filter[updated_by:eq]": user_id.json()["data"][0]["id"]
            }
        )
        if audit is None:
            raise ConnectionError(f'Failed to connect to "{self.url + "/api/pages"}".')

        if audit.status_code != requests.codes.ok:
            raise Exception(f'Failed to get by api "{self.url + "/api/pages"}"'
                            f' with status code {audit.status_code}.')

        log.count_bookstack_changes = audit.json()["total"]  # set the number of changes
