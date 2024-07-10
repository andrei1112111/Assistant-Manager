from src.config import config

from .gitlab import GitLab
from .kimai import Kimai
from .plane import Plane
from .bookstack import BookStack

gitlab_service = GitLab(
    url=config.Gitlab.url,
    token=config.Gitlab.token,
    secret=config.Gitlab.secret_token
)

kimai_service = Kimai(
    url=config.Kimai.url,
    token=config.Kimai.token,
    secret=config.Kimai.secret_token
)

plane_service = Plane(
    url=config.Plane.url,
    token=config.Plane.token,
    secret=config.Plane.secret_token
)

bookStack_service = BookStack(
    url=config.BookStack.url,
    token=config.BookStack.token,
    secret=config.BookStack.secret_token
)

__all__ = [
    "gitlab_service",
    "kimai_service",
    "plane_service",
    "bookStack_service"
]
