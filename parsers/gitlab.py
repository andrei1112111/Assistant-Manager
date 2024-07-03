from __future__ import annotations
from objects import Student, Gitlab, useless_job

import datetime
import requests as rq
import json


HOST = "http://localhost:8080"


def parse_commits(peoples: list[Student]) -> list[int | None]:
    """
    Get commit stats by gitlab api
    :param peoples:
    :return:
    """
    after_date = datetime.datetime.now() - datetime.timedelta(1)  # yesterday
    before_date = datetime.datetime.now() + datetime.timedelta(1)  # tomorrow
    after_date = after_date.strftime("%Y-%m-%d")
    before_date = before_date.strftime("%Y-%m-%d")  # like '2024-03-09'
    # print(after_date.strftime("%Y-%m-%d") + ' -> ' + before_date.strftime("%Y-%m-%d"))
    for student in peoples:
        yield parse_student(student, after_date, before_date)


def parse_student(student: Student, after_date: str, before_date: str) -> int | None:
    """
    Get student commits count on gitlab for the current day
    :param student:
    :param after_date:
    :param before_date:
    :return:
    """
    data = rq.get(
        HOST + f"/api/v4/users/{student.git.username}/events", params={
            "action": "commit",
            "after": after_date,
            "before": before_date
        }
    )
    if data.status_code == rq.codes.ok:
        commit_count = (len(json.loads(data.text)))
        # with open("testing_responces.json", "w") as file:
        #     json.dump(json.loads(data.text), file)
        return commit_count
    else:
        print(f"{student.git.username}: {data.status_code}")


# parse_commits([])

res = parse_commits(
    [
        Student(
            Gitlab("", "root"),
            None,
            None,
            None
        ),
        Student(
            Gitlab("", "testtest"),
            None,
            None,
            None
        ),
        Student(
            Gitlab("", "not_existing_user"),
            None,
            None,
            None
        ),
    ]
)
print([i for i in res])
