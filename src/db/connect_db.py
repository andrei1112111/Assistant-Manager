import logging
from typing import Optional

from sqlalchemy import Connection

from .db import engine
from .entity.base_entity import Base

logger = logging.getLogger("database")
conn: Optional[Connection] = None


def connect_db():
    logger.info("Connect to database")
    engine.connect()

    logger.info("Create schema")
    Base.metadata.create_all(engine)


def disconnect_db():
    logger.info("Disconnect from database")
    if conn is not None:
        conn.close()
