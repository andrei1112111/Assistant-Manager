from scheduler import start_scheduler
from src.logger import logger
from services import plane_service, kimai_service, gitlab_service, bookStack_service, config


def run_app():
    def job():
        from src.db.data_exchange.get_students import get_students_from_db
        from src.db.data_exchange.put_logs import put_logs_to_db

        students = get_students_from_db()

        gitlab_service.get_info_about_students(students)
        kimai_service.get_info_about_students(students)
        plane_service.get_info_about_students(students)
        bookStack_service.get_info_about_students(students)

        put_logs_to_db(students)

    logger.info(f"The scheduler is waiting for {config.time}.")
    start_scheduler(job)


if __name__ == "__main__":
    run_app()
