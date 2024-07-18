from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from src.db.entity import LogDB


class ActionLogRepository:
    def __init__(self, session: Session):
        self.session = session

    def save_all(self, logs: List[LogDB]):
        """
        Adds a list of logs to the database.
        """
        for log in logs:
            self.session.add(log)
        self.session.commit()

    def update_kimai(self, logs: List[LogDB]):
        for log in logs:

            self.session.query(LogDB).filter(
                and_(
                    LogDB.student_id == log.student_id,
                    func.date(LogDB.date) == func.date(log.date)
                )
            ).update({'count_kimai_hours': log.count_kimai_hours, 'date': log.date})

        self.session.commit()
