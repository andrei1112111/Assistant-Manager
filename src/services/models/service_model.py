from src.logger import logger
from .student_model import Student


class Service:
    def __init__(self, url, token, secret):
        self.url = url
        self.token = token
        self.secret = secret

    def get_info_about_students(self):
        from src.db.data_exchange.get_students import get_students_from_db
        from src.db.data_exchange.put_logs import put_logs_to_db

        students = get_students_from_db()

        for student in students:
            connected = self.parse_student_activity(student)

            if connected is False:  # failed to connect or use api
                return  # stop working

            # else: Successful data acquisition

        put_logs_to_db(students)

        logger.info(f"Statistics about students on {self.__name__} successfully loaded.")

    def parse_student_activity(self, student: Student) -> bool:
        pass
