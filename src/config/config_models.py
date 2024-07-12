from __future__ import annotations

from pydantic import BaseModel
import datetime
import pytz


class ServiceApiConfigModel(BaseModel):
    url: str  # like 'http://localhost:8080'
    token: str | None
    secret_token: str | None


class PostgresConfigModel(BaseModel):
    host: str
    port: str
    user: str
    password: str
    db: str


class ConfigModel(BaseModel):
    timezone: pytz.BaseTzInfo  # like 'Asia/Novosibirsk'
    schedule_time: datetime.datetime  # like '18:00'

    # All students will be processed in parts of package_of_students_size
    package_of_students_size: int  # the number of students processed at one part.

    Postgres: PostgresConfigModel
    Gitlab: ServiceApiConfigModel
    Kimai: ServiceApiConfigModel
    Plane: ServiceApiConfigModel
    BookStack: ServiceApiConfigModel

    class Config:  # this is necessary to allow pydantic to work with data types from other libraries
        arbitrary_types_allowed = True
