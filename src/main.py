from services import plane_service, kimai_service, gitlab_service, bookStack_service
from src.db.repository import students_repository, action_log_repository
from src.logger import logger
from src.db.entity import LogDB
from src.config import config

from scheduler import start_scheduler


def run_app():
    def job():
        offset = 0

        # get package of active students from bd
        students = students_repository.get_active_user(limit=config.package_of_students_size, offset=offset)

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
            action_log_repository.save_all(logs)

            # get next package of students
            offset += config.package_of_students_size
            students = students_repository.get_active_user(limit=config.package_of_students_size, offset=offset)

        # when the packages are over, reset the offset for correct further getting students
        students_repository.clear_offset()

    logger.info(f"The scheduler is waiting for {config.schedule_time.hour}:{config.schedule_time.minute}.")
    start_scheduler(job)


if __name__ == "__main__":
    run_app()
