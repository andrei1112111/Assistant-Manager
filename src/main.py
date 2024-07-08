from scheduler import start_scheduler
from logger import info
from services import plane_service, kimai_service, gitlab_service, bookStack_service, config


def run_app():
    def job():
        gitlab_service.get_info_about_students()
        kimai_service.get_info_about_students()
        plane_service.get_info_about_students()
        bookStack_service.get_info_about_students()

    info(f"The scheduler is waiting for {config.time}.")
    start_scheduler(job)


if __name__ == "__main__":
    run_app()
