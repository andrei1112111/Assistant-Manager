from .students_repository import StudentRepository
from .logbook_repository import LogbookRepository
from ..session import Session

students_repository = StudentRepository(Session())
logbook_repository = LogbookRepository(Session())

__all__ = [
    "students_repository",
    "logbook_repository"
]
