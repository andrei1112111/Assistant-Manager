from typing import List

from ..session import bd_session
from ..entity.student_entity import StudentDB
from src.services.models.student_model import Student
from src.logger import logger


def get_students_from_db() -> List[Student]:
    # get all Students from db
    students_db = bd_session.query(StudentDB).all()
    students = []
    for student_db in students_db:  # transfer data StudentDB -> Student for Services
        if student_db.is_active is True:
            student = Student(
                    id=student_db.id,
                    name=student_db.name + " " + student_db.surname,

                    GitLab_username=None,
                    Plane_workspace=None,
                    Bookstack_username=None,
                    Kimai_username=None,

                    commits_count=-1,
                    worked_time=-1,
                    active_tasks=["none"],
                    bookstack_changes=-1
                )

            if "gitlab" in student_db.logins.keys():
                student.GitLab_username = student_db.logins["gitlab"]
            if "plane" in student_db.logins.keys():
                student.Plane_workspace = student_db.logins["plane"]
            if "bookstack" in student_db.logins.keys():
                student.Bookstack_username = student_db.logins["bookstack"]
            if "kimai" in student_db.logins.keys():
                student.Kimai_username = student_db.logins["kimai"]

            students.append(student)

    logger.info(f"Information about students has been received successfully. Received {len(students_db)} students.")

    return students
