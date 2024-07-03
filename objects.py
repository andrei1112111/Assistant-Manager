def useless_job():
    from time import sleep, localtime
    current_time = localtime()
    print("I'm working...")
    print(f"It's {current_time.tm_hour}:{current_time.tm_min}:{current_time.tm_sec}")
    sleep(5)


class Gitlab:
    def __init__(self, proj_repo: str, username: str):
        self.proj_repo = proj_repo
        self.username = username


class Kimai:
    pass


class BookStack:
    pass


class Plane:
    pass


class Student:
    def __init__(self, gitlab, plane, bookstack, kimai):
        self.git = gitlab
        self.plane = plane
        self.bookstack = bookstack
        self.kimai = kimai
