from typing import List

from parsers.bookstack import parse_activity
from parsers.gitlab import parse_commits
from parsers.kimai import parse_active_hours
from parsers.plane import parse_active_tasks
from common.common import Student, check_config, check_env_vars, parse_db

from time import sleep
from configparser import ConfigParser
import threading
import schedule
import logging
import sys
import os


def run_threaded(job_func, peoples: List[Student], host: str, token: str, secret: str):
    job_thread = threading.Thread(
        target=job_func,
        args=(peoples, host, token, secret, )
    )
    job_thread.start()


def parse_data(data):
    """
    Parse user activity from Bookstack, commits from GitLab, active tasks from Plane, active hours from Kimai
    and put it into Postgres db
    """
    logging.info(f"Script is getting data...")
    students = parse_db()
    for task, host, token, secret in [
        (parse_activity, data["bsH"], data["bsT"], data["bsS"]),
        (parse_commits, data["glH"], "", ""),
        (parse_active_tasks, data["plH"], data["plT"], ""),
        (parse_active_hours, data["kmH"], data["kmT"], "")
    ]:
        run_threaded(task, students, host, token, secret)
    while threading.active_count() != 1:
        sleep(1)
    logging.info(f"Script is waiting for {schedule_time} by {timezone}...")


logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    level=logging.DEBUG
)
config = ConfigParser()

schedule_time: str
timezone: str
configuration: dict
if len(sys.argv) >= 2 and sys.argv[1] in ["-c", "--config"]:
    check_config("./config/settings.ini")
    config.read("./config/settings.ini")
    schedule_time = config['Time']['schedule_time']
    timezone = config['Time']['timezone']
    configuration = {
        "sh": schedule_time,
        "tz": timezone,
        "plH": config['Services hosts']['plane'],
        "bsH": config['Services hosts']['bookstack'],
        "kmH": config['Services hosts']['kimai'],
        "glH": config['Services hosts']['gitlab'],
        "plT": config['API Tokens']['plane_token'],
        "bsT": config['API Tokens']['bookstack_token_id'],
        "kmT": config['API Tokens']['kimai_token'],
        "bsS": config['API Tokens']['bookstack_token_secret'],
    }
else:
    check_env_vars()
    schedule_time = os.environ.get("schedule_time")
    timezone = os.environ.get("TIMEZONE")
    configuration = {
        "sh": schedule_time,
        "tz": timezone,
        "plH": os.environ.get("PLANE"),
        "bsH": os.environ.get("BOOKSTACK"),
        "kmH": os.environ.get("KIMAI"),
        "glH": os.environ.get("GITLAB"),
        "plT": os.environ.get("PLANE_TOKEN"),
        "bsT": os.environ.get("BOOKSTACK_TOKEN"),
        "kmT": os.environ.get("KIMAI_TOKEN"),
        "bsS": os.environ.get("BOOKSTACK_SECRET"),
    }

schedule.every().day.at(schedule_time, timezone).do(parse_data, configuration)

parse_data(configuration)
while True:
    schedule.run_pending()
    sleep(1)
