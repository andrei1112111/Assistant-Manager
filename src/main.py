from services import plane_service, kimai_service, gitlab_service, bookStack_service
from src.db.repository import students_repository, action_log_repository
from src.logger import logger
from src.db.entity import LogDB
from src.config import config

from scheduler import start_scheduler
from datetime import datetime
from pytz import timezone


def run_app():
    def job():
        # current_date = datetime.now(tz=timezone(str(config.timezone)))  # current date
        for i in range(2, 30, 1):
            current_date = datetime(year=2024, month=7, day=i)
            if current_date.weekday() < 5:  # only | 0-4 | mon-fri |
                logger.info(f"?>------------------{current_date}------------------?>")

                offset = 0
                while True:  # while package is not empty
                    # get package of active students from bd
                    students = students_repository.get_active_users(limit=config.package_of_students_size,
                                                                    offset=offset)

                    if len(students) == 0:  # There are no more students in the database
                        logger.info("All students have been successfully processed")
                        break

                    logMap = dict()
                    for student in students:  # empty logs for students (one log for one student)
                        logMap[student.id] = LogDB(student_id=student.id)

                        # fill logs with activities
                        for service in [plane_service, kimai_service, gitlab_service, bookStack_service]:
                            try:
                                service.fill_student_activity(student, logMap[student.id], current_date)

                            except Exception as fail_reason:
                                # add fail_reason to log.fail_reasons
                                if logMap[student.id].fail_reasons is None:
                                    logMap[student.id].fail_reasons = ""

                                msg = f"|{service.__class__.__name__}: {fail_reason}|"
                                logMap[student.id].fail_reasons += msg
                                logger.warning(msg)

                        logger.info(
                            f"{student.name}: {logMap[student.id].plane_tasks}|"
                            f"{logMap[student.id].count_kimai_hours}|{logMap[student.id].count_bookstack_changes}|"
                            f"{logMap[student.id].count_gitlab_commits}")

                    # push logs to db
                    action_log_repository.save_all(
                        logMap.values(),
                        current_date
                    )

                    # shift offset to get the next package
                    offset += config.package_of_students_size
                logger.info("logged")

    job()

    # logger.info(f"The scheduler is waiting for "
    #             f"{str(config.schedule_time.hour).zfill(2)}:{str(config.schedule_time.minute).zfill(2)}.")
    #
    # start_scheduler(job)


if __name__ == "__main__":
    run_app()
