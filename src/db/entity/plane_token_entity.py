from sqlalchemy import Column, TEXT

from .base_entity import Base


class PlaneTokenDB(Base):
    __tablename__ = "plane_tokens_list"

    workspace = Column(
        TEXT, primary_key=True
    )
    token = Column(
        TEXT
    )
