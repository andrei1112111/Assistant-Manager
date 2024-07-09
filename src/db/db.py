from src.logger import logger

from sqlalchemy import create_engine

from src.config import config

logger.getLogger("sqlalchemy.engine.Engine.engine")
engine = create_engine(
    "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        config.postgres.user,
        config.postgres.password,
        config.postgres.host,
        config.postgres.port,
        config.postgres.db,
    ),
    # pool_size=5,
    # max_overflow=10,
    # echo=config.server.debug,
    # pool_logging_name="engine",
    # logging_name="engine",
)
