from sqlalchemy import Column, INTEGER, TEXT, TIMESTAMP

from .base_entity import Base


class PeopleCountLogDB(Base):
    __tablename__ = "people_count_logs"
    date = Column(
        TIMESTAMP, primary_key=True
    )
    count = Column(
        INTEGER
    )
    room = Column(
        TEXT
    )
