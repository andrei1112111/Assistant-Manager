from __future__ import annotations
from typing_extensions import Annotated
from pydantic import BaseModel, AfterValidator
from .config_validators import *

TimezoneType = Annotated[str, AfterValidator(validate_timezone)]  # annotated type for validation field

Schedule_timeType = Annotated[str, AfterValidator(validate_schedule_time)]  # also annotated type for validation field


class TimeConfig(BaseModel):
    timezone: TimezoneType
    schedule_time: Schedule_timeType


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
