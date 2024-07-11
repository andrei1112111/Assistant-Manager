from .students_repository import StudentRepository
from .logbook_repository import LogbookRepository
from src.config import config
from ..session import Session

students_repository = StudentRepository(Session())
logbook_repository = LogbookRepository(Session())

#  package_of_students_size is a part of the students progressed at one time
students_repository.set_package_size(config.package_of_students_size)

__all__ = [
    "students_repository",
    "logbook_repository"
]
