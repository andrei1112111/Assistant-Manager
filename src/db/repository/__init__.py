from .student_repository import StudentRepository
from .activity_log_repository import ActionLogRepository
from .people_count_log_repository import PeopleCountLogRepository
from .plane_tokens_list_repository import PlaneTokensListRepository

from ..session import Session

students_repository = StudentRepository(Session())
action_log_repository = ActionLogRepository(Session())
people_count_log_repository = PeopleCountLogRepository(Session())
plane_tokens_list_repository = PlaneTokensListRepository(Session())

__all__ = [
    "students_repository",
    "action_log_repository",
    "people_count_log_repository",
    "plane_tokens_list_repository"
]
