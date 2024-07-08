import os
import src.logger as logger
from dotenv import load_dotenv
from pydantic import ValidationError

from .config_models import ConfigModel


def load_config() -> ConfigModel:
    load_dotenv()  # load variables from .env

    config_data: dict = {
        "time": {
            "timezone": os.getenv("TIMEZONE"),
            "schedule_time": os.getenv("SCHEDULE_TIME"),
        },
        "postgres": {
            "host": os.getenv("POSTGRES_HOST"),
            "port": os.getenv("POSTGRES_PORT"),
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
            "db": os.getenv("POSTGRES_DB"),
        },
        "Gitlab": {
            "url": os.getenv("GITLAB_URL"),
            "token": None,
            "secret_token": None
        },
        "Kimai": {
            "url": os.getenv("KIMAI_URL"),
            "token": os.getenv("KIMAI_TOKEN"),
            "secret_token": None
        },
        "Plane": {
            "url": os.getenv("PLANE_URL"),
            "token": os.getenv("PLANE_TOKEN"),
            "secret_token": None
        },
        "BookStack": {
            "url": os.getenv("BOOKSTACK_URL"),
            "token": os.getenv("BOOKSTACK_TOKEN"),
            "secret_token": os.getenv("BOOKSTACK_SECRET_TOKEN")
        },
    }

    # Validate config
    try:
        config_model = ConfigModel(**config_data)
    except ValidationError as err_msg:
        logger.critical(f"Config has not been loaded. An exception: {err_msg}.")
        exit(6)

    logger.info("Config successfully loaded.")

    return config_model
