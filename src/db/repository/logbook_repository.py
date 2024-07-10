from typing import List

from sqlalchemy.orm import Session

from src.db.entity import LogDB


class LogbookRepository:
    def __init__(self, session: Session):
        self.session = session

    def save_all(self, logs: List[LogDB]):
        """
        Adds a list of logs to the database.
        """
        for log in logs:
            self.session.add(log)

        self.session.commit()
