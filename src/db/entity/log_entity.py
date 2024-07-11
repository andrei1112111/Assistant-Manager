from sqlalchemy import Column, UUID, INTEGER, DATE, TEXT, FLOAT, func
from datetime import datetime
from pytz import timezone

from .base_entity import Base
from src.config import config


def now_in_timezone():
    """
    Now time in timezone from config
    """
    return datetime.now(
        tz=timezone(str(config.timezone))
    )


class LogDB(Base):
    __tablename__ = "logbook"

    # id = Column(
    #     INTEGER, primary_key=True, autoincrement='auto', unique=True, default=0
    # )
    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid(), default=func.gen_random_uuid()
    )
    student_id = Column(
        UUID(as_uuid=True)
    )
    date = Column(
        DATE, default=now_in_timezone, onupdate=now_in_timezone
    )
    plane_tasks = Column(
        TEXT, default=""
    )
    count_gitlab_commits = Column(
        INTEGER, default=0
    )
    count_bookstack_changes = Column(
        INTEGER, default=0
    )
    count_kimai_hours = Column(
        FLOAT, default=0
    )
    fail_reasons = Column(
        TEXT, default=""
    )
