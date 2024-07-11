from __future__ import annotations
from typing import List

from src.db.entity import LogDB, StudentDB
from src.logger import logger


class BaseService:
    def __init__(self, url, token, secret):
        self.url: str = url
        self.token: str = token
        self.secret: str = secret

    def put_students_activity_to_logs(self, students: List[StudentDB], logMap: dict[LogDB]):
        """
        For each student and log fill log column appropriate service.
        Add fail_reason when it fails with fill student activity
        """
        # for each student and log
        for student in students:
            try:
                self.fill_student_activity(student, logMap[student.id])

            except Exception as fail_reason:
                if logMap[student.id].fail_reasons is None:
                    logMap[student.id].fail_reasons = ""

                # add fail_reason to log.fail_reasons
                logMap[student.id].fail_reasons += f"|{self.__class__.__name__}: {fail_reason}|"
                logger.warning(f"{self.__class__.__name__}: {fail_reason}")

                # if fail_reason == ConnectionError:
                #     return  # stop parsing if there is no connection to the server

    def fill_student_activity(self, student: StudentDB, log: LogDB):
        """
        Accesses the api to get data about user activity on the service.
        In case of an error, function raise it.
        """
        pass
