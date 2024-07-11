from __future__ import annotations
from typing import List

from src.db.entity import LogDB, StudentDB
from src.logger import logger


class BaseService:
    def __init__(self, url, token, secret):
        self.url: str = url
        self.token: str = token
        self.secret: str = secret

    def put_students_activity_to_logs(self, students: List[StudentDB], logs: List[LogDB]):
        """
        For each student and log fill log column appropriate service.
        Add fail_reason when it fails with fill student activity
        """
        # for each student and log
        for student, log in zip(students, logs):
            fail_reason = self.fill_student_activity(student, log)

            if fail_reason:
                if log.fail_reasons is None:
                    log.fail_reasons = ""

                # add fail_reason to log.fail_reasons
                log.fail_reasons += f"|{self.__class__.__name__}: {fail_reason}|"
                logger.warning(f"{self.__class__.__name__}: {fail_reason}")

    def fill_student_activity(self, student: StudentDB, log: LogDB) -> str | None:
        """
        Accesses the api to get data about user activity on the service.
        In case of an error, it returns it as string else None.
        """
        pass
