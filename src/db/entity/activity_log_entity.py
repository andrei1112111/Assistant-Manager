from sqlalchemy import Column, INTEGER, DATE, TEXT, FLOAT
import datetime
from pytz import timezone

from .base_entity import Base
from src.config import config


def now_in_timezone():
    """
    Now time in timezone from config
    """
    return datetime.datetime.now(
        tz=timezone(str(config.timezone))
    )


class ActivityLogDB(Base):
    __tablename__ = "logbook"

    id = Column(
        INTEGER, primary_key=True
    )
    student_id = Column(
        INTEGER
    )
    date = Column(
        DATE, default=now_in_timezone, onupdate=now_in_timezone
    )
    plane_tasks = Column(
        TEXT, default=None
    )
    count_gitlab_commits = Column(
        INTEGER, default=None
    )
    count_bookstack_changes = Column(
        INTEGER, default=None
    )
    count_kimai_hours = Column(
        FLOAT, default=None
    )
    fail_reasons = Column(
        TEXT, default=None
    )
