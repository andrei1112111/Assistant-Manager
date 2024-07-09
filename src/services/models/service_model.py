from typing import List

from src.logger import logger
from .student_model import Student


class Service:
    def __init__(self, url, token, secret):
        self.url = url
        self.token = token
        self.secret = secret

    def get_info_about_students(self, students: List[Student]):
        for student in students:
            connected = self.parse_student_activity(student)

            if connected is False:  # failed to connect or use api
                return  # stop working

            # else: Successful data acquisition

        logger.info(f"Statistics about students on {self.__class__.__name__} successfully loaded.")

    def parse_student_activity(self, student: Student) -> bool:
        pass
