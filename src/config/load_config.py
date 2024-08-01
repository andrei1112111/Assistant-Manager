from dotenv import load_dotenv
import datetime
import pytz
import os

from .config_models import ConfigModel


def load_config() -> ConfigModel:
    load_dotenv()  # load variables from .env

    config_data: dict = {
        "timezone": pytz.timezone(os.getenv("TIMEZONE")),
        "schedule_time": datetime.datetime.strptime(os.getenv("SCHEDULE_TIME"), "%H:%M"),
        "package_of_students_size": int(os.getenv("PROCESSING_POCKET_SIZE")),
        "Postgres": {
            "host": os.getenv("POSTGRES_HOST"),
            "port": os.getenv("POSTGRES_PORT"),
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
            "db": os.getenv("POSTGRES_DB"),
        },
        "Gitlab": {
            "url": os.getenv("GITLAB_URL"),
            "token": os.getenv("GITLAB_TOKEN"),
            "secret_token": None
        },
        "Kimai": {
            "url": os.getenv("KIMAI_URL"),
            "token": os.getenv("KIMAI_TOKEN"),
            "secret_token": None
        },
        "Plane": {
            "url": os.getenv("PLANE_URL"),
            "token": None,
            "secret_token": None
        },
        "BookStack": {
            "url": os.getenv("BOOKSTACK_URL"),
            "token": os.getenv("BOOKSTACK_TOKEN"),
            "secret_token": os.getenv("BOOKSTACK_SECRET_TOKEN"),
        },
        "RESTAPI": {
            "host": os.getenv("RESTAPI_HOST"),
            "port": os.getenv("RESTAPI_PORT"),
            "auth_key": os.getenv("RESTAPI_AUTH_KEY"),
        },
        "schedule_plane": {
            "begin_hour": os.getenv("SCHEDULER_PLANE_BEGIN_HOUR"),
            "last_hour": os.getenv("SCHEDULER_PLANE_LAST_HOUR"),
            "interval_minute": os.getenv("SCHEDULER_PLANE_INTERVAL_MINUTE"),
        },
    }

    # The package size is too large
    if config_data["package_of_students_size"] > 200:
        config_data["package_of_students_size"] = 200

    # Validate config
    config_model = ConfigModel(**config_data)

    return config_model  # config successfully loaded
