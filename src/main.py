from services import plane_service, kimai_service, gitlab_service, bookStack_service
from src.db.repository import students_repository, logbook_repository
from src.logger import logger
from src.db.entity import LogDB
from src.config import config

from scheduler import start_scheduler


def run_app():
    def job():
        # get active students from bd
        students = students_repository.find_all_by_is_active(True)

        logs = [LogDB() for _ in range(len(students))]  # empty logs for all students

        # for each student and log, set log.student_id = student.id
        for student, log in zip(students, logs):
            log.student_id = student.id

        # fill logs with activities
        plane_service.put_students_activity_to_logs(students, logs)
        kimai_service.put_students_activity_to_logs(students, logs)
        gitlab_service.put_students_activity_to_logs(students, logs)
        bookStack_service.put_students_activity_to_logs(students, logs)

        # save all logs
        logbook_repository.save_all(logs)

    job()
    logger.info(f"The scheduler is waiting for {config.schedule_time}.")
    start_scheduler(job)


if __name__ == "__main__":
    run_app()
