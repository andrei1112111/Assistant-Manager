from typing import Optional

from sqlalchemy import Connection

from .db import engine
from .entity.base_entity import Base
from src.logger import logger

conn: Optional[Connection] = None


def connect_db():
    logger.info("Connect to database")
    engine.connect()

    Base.metadata.create_all(engine)


def disconnect_db():
    logger.info("Disconnect from database")
    if conn is not None:
        conn.close()
