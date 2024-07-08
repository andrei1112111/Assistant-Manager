from sqlalchemy import Column, UUID, func, INTEGER, DATE, TEXT

from .base_entity import Base

from datetime import datetime


class LogDB(Base):
    __tablename__ = "logbook"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    student_id = Column(INTEGER)
    date = Column(DATE, default=datetime.now, onupdate=datetime.now)
    plane_tasks = Column(TEXT)
    count_gitlab_commits = Column(INTEGER)
    count_bookstack_changes = Column(INTEGER)
    count_kimai_hours = Column(INTEGER)
