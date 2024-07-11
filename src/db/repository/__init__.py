from .students_repository import StudentRepository
from .action_log_repository import ActionLogRepository
from src.config import config
from ..session import Session

students_repository = StudentRepository(Session())
action_log_repository = ActionLogRepository(Session())

__all__ = [
    "students_repository",
    "action_log_repository"
]
