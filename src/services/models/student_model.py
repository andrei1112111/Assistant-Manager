from typing import List
from dataclasses import dataclass


@dataclass
class Student:
    id: int
    name: str

    GitLab_username: str
    Kimai_username: str
    Plane_workspace: str
    Bookstack_username: str

    commits_count: int
    worked_time: int  # in minutes
    active_tasks: List[str]
    bookstack_changes: int  # number of changes
