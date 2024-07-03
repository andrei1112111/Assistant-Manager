from src.parsers.bookstack import parse_activity
from src.parsers.gitlab import parse_commits
from src.parsers.kimai import parse_active_hours
from src.parsers.plane import parse_active_tasks
from src.additional import Student

from time import sleep
import configparser
import threading
import schedule
import logging
import sys

logging.getLogger('').addHandler(logging.StreamHandler(sys.stdout))
logging.getLogger('').setLevel(logging.INFO)

config = configparser.ConfigParser()
config.read("config/settings.ini")


def run_threaded(job_func, peoples):
    job_thread = threading.Thread(
        target=job_func,
        args=(peoples, )
    )
    job_thread.start()


# students for testing
students = [
    Student(
        "root",
        "None",
        None,
        None
    ),
    Student(
        "testtest",  # gitlub nickname
        "testingworkspace",  # ? plane workspace name
        None,
        None
    ),
    Student(
        "not_existing_user",
        None,
        None,
        None
    ),
]
# -

schedule.every().day.at(config['Time']['wakeup time'], config['Time']['timezone']).do(
    run_threaded, parse_activity,
    students,
)  # task for bookstack

schedule.every().day.at(config['Time']['wakeup time'], config['Time']['timezone']).do(
    run_threaded, parse_commits,
    students,
)  # task for gitlab

schedule.every().day.at(config['Time']['wakeup time'], config['Time']['timezone']).do(
    run_threaded, parse_active_tasks,
    students,
)  # task for plane

schedule.every().day.at(config['Time']['wakeup time'], config['Time']['timezone']).do(
    run_threaded, parse_active_hours,
    students,
)  # task for kimai

while True:
    schedule.run_pending()
    sleep(1)


# run_threaded(parse_commits, students)
