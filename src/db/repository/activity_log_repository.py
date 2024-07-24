from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from src.db.entity import ActivityLogDB


class ActionLogRepository:
    def __init__(self, session: Session):
        self.session = session

    def save_all(self, logs: List[ActivityLogDB]):
        """
        Adds a list of logs to the database.
        """
        for log in logs:
            self.session.add(log)
        self.session.commit()

    def update_kimai(self, logs: List[ActivityLogDB]):
        for log in logs:

            self.session.query(ActivityLogDB).filter(
                and_(
                    ActivityLogDB.student_id == log.student_id,
                    func.date(ActivityLogDB.date) == func.date(log.date)
                )
            ).update({'count_kimai_hours': log.count_kimai_hours, 'date': log.date})

        self.session.commit()
