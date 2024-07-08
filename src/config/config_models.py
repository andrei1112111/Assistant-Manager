from __future__ import annotations
from typing_extensions import Annotated
from pydantic import BaseModel, AfterValidator
from .config_validators import *

TimezoneT = Annotated[str, AfterValidator(validate_timezone)]

Schedule_timeT = Annotated[str, AfterValidator(validate_schedule_time)]


class TimeConfig(BaseModel):
    timezone: TimezoneT
    schedule_time: Schedule_timeT


class ServiceApiConfigModel(BaseModel):
    url: str
    token: str | None
    secret_token: str | None


class PostgresConfigModel(BaseModel):
    host: str
    port: str
    user: str
    password: str
    db: str


class ConfigModel(BaseModel):
    time: TimeConfig
    postgres: PostgresConfigModel
    Gitlab: ServiceApiConfigModel
    Kimai: ServiceApiConfigModel
    Plane: ServiceApiConfigModel
    BookStack: ServiceApiConfigModel
