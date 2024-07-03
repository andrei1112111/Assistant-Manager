from parsers.gitlab import parse_commits
from parsers.kimai import parse_active_hours
from parsers.plane import parse_active_tasks
from parsers.bookstack import parse_activity

from time import sleep
import threading
import schedule

DEBUG = True


class Time:
    hour: int
    minute: int


def run_threaded(job_func, peoples):
    job_thread = threading.Thread(
        target=job_func,
        args=(peoples, )
    )
    job_thread.start()


time = Time()


# -
timezone = "Asia/Novosibirsk"
time.hour, time.minute = 17, 13
students = []
# -

schedule.every().day.at(
    f"{time.hour:02}:{time.minute:02}", timezone).do(run_threaded, parse_activity, students)  # bookstack

schedule.every().day.at(
    f"{time.hour:02}:{time.minute:02}", timezone).do(run_threaded, parse_commits, students)  # gitlab

schedule.every().day.at(
    f"{time.hour:02}:{time.minute:02}", timezone).do(run_threaded, parse_active_tasks, students)  # plane

schedule.every().day.at(
    f"{time.hour:02}:{time.minute:02}", timezone).do(run_threaded, parse_active_hours, students)  # kimai


if DEBUG:
    # run_threaded(parse_active_hours, students)
    # for f in [parse_activity, parse_commits, parse_active_tasks, parse_active_hours]:
    #     run_threaded(f, students)
    pass

while True:
    schedule.run_pending()
    sleep(1)
