from sqlalchemy import Column, BOOLEAN, INTEGER, TEXT
from sqlalchemy.dialects.postgresql import JSON

from .base_entity import Base


class StudentDB(Base):
    __tablename__ = "students"

    id = Column(
        INTEGER, primary_key=True
    )
    name = Column(
        TEXT
    )
    surname = Column(
        TEXT
    )
    logins = Column(
        JSON
    )
    is_active = Column(
        BOOLEAN
    )
    project_id = Column(
        INTEGER
    )
