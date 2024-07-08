from sqlalchemy import Column, UUID, BOOLEAN, VARCHAR, func, INTEGER
from sqlalchemy.dialects.postgresql import JSON

from .base_entity import Base


class StudentDB(Base):
    __tablename__ = "students"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    name = Column(VARCHAR(100))
    surname = Column(VARCHAR(100))
    logins = Column(JSON)
    is_active = Column(BOOLEAN)
    project_id = Column(INTEGER)
