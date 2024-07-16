from typing import List

from sqlalchemy.orm import Session

from src.db.entity import LogDB
from datetime import datetime


class ActionLogRepository:
    def __init__(self, session: Session):
        self.session = session

    def save_all(self, logs: List[LogDB], current_date: datetime):
        """
        Adds a list of logs to the database.
        """
        for log in logs:
            log.date = current_date
            self.session.add(log)
        self.session.commit()
