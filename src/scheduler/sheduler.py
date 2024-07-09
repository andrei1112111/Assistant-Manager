from apscheduler.schedulers.blocking import BlockingScheduler
from src.config import config

scheduler = BlockingScheduler()


def start_scheduler(func):
    schedule_time = config.time.schedule_time.split(':')  # [hour, minute]
    #  len(schedule_time) == 2 since config.time.schedule_time been validated by load_config

    scheduler.add_job(
        func,
        'cron',
        day_of_week='mon-fri',
        hour=int(schedule_time[0]),
        minute=int(schedule_time[1]),
        timezone=config.time.timezone
    )

    scheduler.start()


def stop_scheduler():
    scheduler.shutdown()
