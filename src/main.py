from scheduler import start_scheduler
from src.logger import logger
from services import plane_service, kimai_service, gitlab_service, bookStack_service, config
from src.db import disconnect_db


def run_app():
    def job():
        gitlab_service.get_info_about_students()
        kimai_service.get_info_about_students()
        plane_service.get_info_about_students()
        bookStack_service.get_info_about_students()

    logger.info(f"The scheduler is waiting for {config.time}.")
    start_scheduler(job)


if __name__ == "__main__":
    try:
        run_app()
    except KeyboardInterrupt:
        disconnect_db()
