from __future__ import annotations

from src.db.entity import ActivityLogDB, StudentDB


class BaseService:
    def __init__(self, url, token, secret):
        self.url: str = url
        self.token: str | None = token
        self.secret: str | None = secret

    def fill_student_activity(self, student: StudentDB, log: ActivityLogDB):
        """
        Accesses the api to get data about user activity on the service.
        In case of an error, function raises it.
        """
        pass
