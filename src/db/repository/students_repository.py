from typing import List, Type

from src.db.entity import StudentDB

from sqlalchemy.orm import Session


class StudentRepository:
    def __init__(self, session: Session):
        self.session = session
        self.package_size = 1
        self.offset = 0

    def get_package_by_is_active(self, is_active: bool) -> List[Type[StudentDB]]:
        """
        get next package of students with student.is_active == is_active of package_size
        """
        query = self.session.query(StudentDB).filter(StudentDB.is_active == is_active)

        query = query.offset(self.offset)
        query = query.limit(self.package_size)
        self.offset += self.package_size

        return query.all()

    def set_package_size(self, size):
        """
        just set package_size = size
        """
        self.package_size = size

    def clear_offset(self):
        self.offset = 0
