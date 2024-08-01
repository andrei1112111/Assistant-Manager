from apscheduler.schedulers.blocking import BlockingScheduler

from src.config import config

scheduler = BlockingScheduler()


def start_scheduler(func):
    """
    Add cron job on every monday-friday days in schedule_time by timezone from config
    """
    scheduler.add_job(
        func,
        'cron',
        day_of_week='mon-fri',
        hour=config.schedule_time.hour,
        minute=config.schedule_time.minute,
        timezone=config.timezone
    )

    scheduler.start()


def add_plane_scheduler(func):
    scheduler.add_job(
        func,
        'cron',
        day_of_week='mon-fri',
        hour=f"{config.schedule_plane.begin_hour}-{config.schedule_plane.last_hour}/1",
        timezone=config.timezone,
    )


def stop_scheduler():
    scheduler.shutdown()
