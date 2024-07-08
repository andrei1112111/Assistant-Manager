from typing import List

from ..session import Session
from ..db import engine
from ..entity.log_entity import LogDB
from src.services.models.service_model import Student
from src.logger import info


def put_logs_to_db(students: List[Student]):
    with Session(autoflush=False, bind=engine) as db:
        for student in students:
            log = LogDB(
                student_id=student.id,
                plane_tasks=', '.join(student.active_tasks),
                count_gitlab_commits=student.commits_count,
                count_bookstack_changes=student.bookstack_changes,
                count_kimai_hours=student.worked_time,
            )
            db.add(log)

        db.commit()

        info("Information about students has been uploaded successfully")
