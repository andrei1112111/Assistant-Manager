from typing import List

from ..session import bd_session
from ..entity.student_entity import StudentDB
from src.services.models.student_model import Student
from src.logger import info


def get_students_from_db() -> List[Student]:
    # get all objects
    students_db = bd_session.query(StudentDB).all()
    students = []

    for student_db in students_db:
        students.append(
            Student(
                id=student_db.id,
                name=student_db.name,

                GitLab_username=student_db.logins["gitlab"],
                Plane_workspace=student_db.logins["plane"],
                Bookstack_username=student_db.logins["bookstack"],
                Kimai_username=student_db.logins["kimai"],

                commits_count=0,
                worked_time=0,
                active_tasks=[],
                bookstack_changes=0
            )
        )

    info("Information about students has been received successfully")

    return students
