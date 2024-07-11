from services import plane_service, kimai_service, gitlab_service, bookStack_service
from src.db.repository import students_repository, logbook_repository
from src.logger import logger
from src.db.entity import LogDB
from src.config import config

from scheduler import start_scheduler


def run_app():
    def job():
        # get package of active students from bd
        students = students_repository.get_package_by_is_active(True)

        while students:  # while package is not empty
            logs = [LogDB() for _ in range(len(students))]  # empty logs for students (one log for one student)

            # for each student and log, set log.student_id = student.id
            for student, log in zip(students, logs):
                log.student_id = student.id

            # fill logs with activities
            plane_service.put_students_activity_to_logs(students, logs)
            kimai_service.put_students_activity_to_logs(students, logs)
            gitlab_service.put_students_activity_to_logs(students, logs)
            bookStack_service.put_students_activity_to_logs(students, logs)

            # push logs to db
            logbook_repository.save_all(logs)

            # get next package of students
            students = students_repository.get_package_by_is_active(True)

        # when the packages are over, reset the offset for correct further getting students
        students_repository.clear_offset()

    job()
    logger.info(f"The scheduler is waiting for {config.schedule_time}.")
    start_scheduler(job)


if __name__ == "__main__":
    run_app()
