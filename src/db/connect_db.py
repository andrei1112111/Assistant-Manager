from src.logger import logger
from typing import Optional

from sqlalchemy import Connection, exc

from .db import engine
from .entity.base_entity import Base

logger = logger.getLogger("database")
conn: Optional[Connection] = None


def connect_db():
    logger.info("Connect to database")
    # try:
    #     engine.connect()
    # except exc.OperationalError:
    #     logger.critical("Failed to connect to database: Connection refused")
    #     exit()
    engine.connect()

    logger.info("Create schema")
    Base.metadata.create_all(engine)


def disconnect_db():
    logger.info("Disconnect from database")
    if conn is not None:
        conn.close()
