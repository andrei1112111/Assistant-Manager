from typing import List, Type

from src.db.entity import StudentDB

from sqlalchemy.orm import Session


class StudentRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_all_by_is_active(self, is_active: bool) -> List[Type[StudentDB]]:
        """
        Find all students with student.is_active == is_active.
        """
        return self.session.query(StudentDB).filter(StudentDB.is_active == is_active).all()
