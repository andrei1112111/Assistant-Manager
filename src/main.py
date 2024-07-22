from services import plane_service, kimai_service, gitlab_service, bookStack_service
from src.db.repository import students_repository, action_log_repository, people_count_log_repository
from src.logger import logger
from src.db.entity import ActivityLogDB, PeopleCountLogDB
from src.config import config

from scheduler import start_scheduler

from threading import Thread

from flask import Flask, request, abort, send_file

import datetime
import io
import base64
from PIL import Image

app = Flask(__name__)


def get_students_activity_app():
    def job():
        offset = 0

        while True:  # while the package is not empty
            # get a package of active students from bd
            students = students_repository.get_active_users(limit=config.package_of_students_size, offset=offset)

            if len(students) == 0:  # There are no more students in the database
                logger.info("All students have been successfully processed")
                break

            logMap = dict()
            for student in students:  # empty logs for students (one log for one student)
                logMap[student.id] = ActivityLogDB(student_id=student.id)

                # fill logs with activities
                for service in [plane_service, kimai_service, gitlab_service, bookStack_service]:
                    try:
                        service.fill_student_activity(student, logMap[student.id])

                    except Exception as fail_reason:
                        # add fail_reason to log.fail_reasons
                        if logMap[student.id].fail_reasons is None:
                            logMap[student.id].fail_reasons = ""

                        msg = f"|{service.__class__.__name__}: {fail_reason}|"
                        logMap[student.id].fail_reasons += msg
                        logger.warning(msg)

                logLast4days = [ActivityLogDB(student_id=student.id) for _ in range(1, 5)]
                try:
                    kimai_service.fill_student_activity_last4_days(student, logLast4days)
                except Exception as fail_reason:
                    logger.warning(f"on last7days |{kimai_service.__class__.__name__}: {fail_reason}|")

                # logger.info(f"{student.name, student.surname, logLast4days}")
                action_log_repository.update_kimai(logLast4days)

            # push logs to db

            # logger.info(f"{[(i.plane_tasks, i.count_kimai_hours) for i in logMap.values()]}")
            action_log_repository.save_all(
                logMap.values()
            )

            # shift offset to get the next package
            offset += config.package_of_students_size

    logger.info(f"The scheduler is waiting for "
                f"{str(config.schedule_time.hour).zfill(2)}:{str(config.schedule_time.minute).zfill(2)}.")

    start_scheduler(job)


def handle_people_count_post_app():
    @app.route('/api/room_view/<room>', methods=['GET'])
    def get_last_view(room):
        return send_file(f"/opt/bot/tmp/last_{room}_view.png", mimetype='image/gif')

    @app.route('/api/count_logs', methods=['POST'])
    def count_logs():
        if not request.json:
            abort(400)  # bad request

        data = request.json

        auth_key = data.get("auth_key", None)
        room = data.get("room", None)
        count = data.get("count", None)
        date = data.get("date", None)

        if any([i is None for i in [auth_key, room, count, date]]):
            abort(400)  # bad request

        if not (auth_key == config.RESTAPI.auth_key):
            abort(401)  # bad request

        log = PeopleCountLogDB(
            date=datetime.datetime.strptime(date, "%m/%d/%Y, %H:%M:%S"),
            count=count,
            room=room
        )

        if 'image' in request.json:
            # get the base64 encoded string
            im_b64 = request.json['image']

            # convert it into bytes
            img_bytes = base64.b64decode(im_b64.encode('utf-8'))

            # convert bytes data to PIL Image object
            img = Image.open(io.BytesIO(img_bytes))

            img.save(f"tmp/last_{room}_view.png")

        logger.info(f"{log.room, log.count}")
        people_count_log_repository.save(log)

        return {}, 200  # ok

    app.run(debug=False, host=config.RESTAPI.host, port=int(config.RESTAPI.port))


if __name__ == "__main__":
    get_students_activity = Thread(target=get_students_activity_app)
    get_students_activity.start()

    handle_people_count_post = Thread(target=handle_people_count_post_app)
    handle_people_count_post.start()

    get_students_activity.join()
    handle_people_count_post.join()
