from typing import List, Type

from src.db.entity import StudentDB

from sqlalchemy.orm import Session


class StudentRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_active_user(self, limit: int, offset: int) -> List[Type[StudentDB]]:
        """
        get users with is_active = True
        """
        query = self.session.query(StudentDB).filter(StudentDB.is_active is True)

        query = query.offset(offset)
        query = query.limit(limit)

        return query.all()
