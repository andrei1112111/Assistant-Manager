from services import plane_service, kimai_service, gitlab_service, bookStack_service
from src.db.repository import students_repository, action_log_repository
from src.logger import logger
from src.db.entity import LogDB
from src.config import config

from scheduler import start_scheduler


def run_app():
    def job():
        offset = 0

        while True:  # while package is not empty
            # get package of active students from bd
            students = students_repository.get_active_user(limit=config.package_of_students_size, offset=offset)

            if len(students) == 0:  # There are no more students in the database
                logger.info("All students have been successfully processed")
                break

            logMap = dict()
            for student in students:  # empty logs for students (one log for one student)
                logMap[student.id] = LogDB(student_id=student.id)

            # fill logs with activities
            plane_service.put_students_activity_to_logs(students, logMap)
            kimai_service.put_students_activity_to_logs(students, logMap)
            gitlab_service.put_students_activity_to_logs(students, logMap)
            bookStack_service.put_students_activity_to_logs(students, logMap)

            # push logs to db
            action_log_repository.save_all(
                logMap.values()
            )

            # shift offset to get the next package
            offset += config.package_of_students_size

    job()

    logger.info(f"The scheduler is waiting for "
                f"{str(config.schedule_time.hour).zfill(2)}:{str(config.schedule_time.minute).zfill(2)}.")
    start_scheduler(job)


if __name__ == "__main__":
    run_app()
