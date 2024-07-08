import pytz


def validate_timezone(timezone: str) -> str:
    try:
        pytz.timezone(timezone)
    except pytz.exceptions.UnknownTimeZoneError:
        assert isinstance(timezone, pytz.BaseTzInfo), f"Timezone '{timezone}' is invalid"

    return timezone


def validate_schedule_time(time: str) -> str:
    assert (len(time) == 5 or all(
        [
            time[0].isdigit(), time[1].isdigit(), time[2] == ':', time[3].isdigit(), time[4].isdigit()
        ]
    )), f"Schedule time '{time}' is invalid"

    return time
