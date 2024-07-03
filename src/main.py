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


def run_threaded(job_func, peoples, host):
    job_thread = threading.Thread(
        target=job_func,
        args=(peoples, host, )
    )
    job_thread.start()


# students for testing
students = [
    Student(
        "root",
        None,
        None,
        None
    ),
    Student(
        "testtest",
        None,
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

schedule.every().day.at(
    config['Time']['wakeup time'], config['Time']['timezone']
).do(run_threaded, parse_activity, students, config['Services hosts']['bookstack'])  # task for bookstack

schedule.every().day.at(
    config['Time']['wakeup time'], config['Time']['timezone']
).do(run_threaded, parse_commits, students, config['Services hosts']['gitlab'])  # task for gitlab

schedule.every().day.at(
    config['Time']['wakeup time'], config['Time']['timezone']
).do(run_threaded, parse_active_tasks, students, config['Services hosts']['plane'])  # task for plane

schedule.every().day.at(
    config['Time']['wakeup time'], config['Time']['timezone']
).do(run_threaded, parse_active_hours, students, config['Services hosts']['kimai'])  # task for kimai

while True:
    schedule.run_pending()
    sleep(1)


#
# res = parse_commits(students, config['Services hosts']['gitlab'])
# print(res)
