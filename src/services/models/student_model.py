from __future__ import annotations

from typing import List
from dataclasses import dataclass


@dataclass
class Student:
    id: int
    name: str

    GitLab_username: str | None
    Kimai_username: str | None
    Plane_workspace: str | None
    Bookstack_username: str | None

    commits_count: int
    worked_time: int  # in minutes
    active_tasks: List[str]
    bookstack_changes: int  # number of changes
