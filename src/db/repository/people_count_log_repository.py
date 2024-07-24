from sqlalchemy.orm import Session

from src.db.entity import PeopleCountLogDB


class PeopleCountLogRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, log: PeopleCountLogDB):
        self.session.add(log)

        self.session.commit()
