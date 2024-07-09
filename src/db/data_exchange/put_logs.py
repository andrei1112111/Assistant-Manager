from typing import List

from ..session import bd_session
from ..entity.log_entity import LogDB
from src.services.models.service_model import Student
from src.logger import logger


def put_logs_to_db(students: List[Student]):
    for student in students:
        log = LogDB(
            student_id=student.id,
            plane_tasks=', '.join(student.active_tasks),
            count_gitlab_commits=student.commits_count,
            count_bookstack_changes=student.bookstack_changes,
            count_kimai_hours=student.worked_time,
        )
        bd_session.add(log)

    bd_session.commit()

    logger.info("Information about students has been uploaded successfully")
