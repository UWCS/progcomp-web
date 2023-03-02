import re
from datetime import datetime, timedelta

import dateparser


# Stolen from github.com/uwcs/apollo
def parse_time(time, /):
    # dateparser.parse returns None if it cannot parse
    parsed_time = dateparser.parse(
        time, settings={"DATE_ORDER": "DMY", "PREFER_DATES_FROM": "future"}
    )

    now = datetime.now()

    if not parsed_time:
        try:
            parsed_time = datetime.strptime(time, "%Y-%m-%d %H:%M")
        except ValueError:
            pass

    if not parsed_time:
        try:
            parsed_time = datetime.strptime(time, "%m-%d %H:%M")
            parsed_time = parsed_time.replace(year=now.year)
            if parsed_time < now:
                parsed_time = parsed_time.replace(year=now.year + 1)
        except ValueError:
            pass

    if not parsed_time:
        try:
            parsed_time = datetime.strptime(time, "%H:%M:%S")
            parsed_time = parsed_time.replace(
                year=now.year, month=now.month, day=now.day
            )
            if parsed_time < now:
                parsed_time = parsed_time + timedelta(days=1)

        except ValueError:
            pass

    if not parsed_time:
        try:
            parsed_time = datetime.strptime(time, "%H:%M")
            parsed_time = parsed_time.replace(
                year=now.year, month=now.month, day=now.day
            )
            if parsed_time < now:
                parsed_time = parsed_time + timedelta(days=1)
        except ValueError:
            pass

    if not parsed_time:
        result = re.match(r"(\d+d)?\s*(\d+h)?\s*(\d+m)?\s*(\d+s)?(?!^)$", time)
        if result:
            parsed_time = now
            if result.group(1):
                parsed_time = parsed_time + timedelta(days=int(result.group(1)[:-1]))
            if result.group(2):
                parsed_time = parsed_time + timedelta(hours=int(result.group(2)[:-1]))
            if result.group(3):
                parsed_time = parsed_time + timedelta(minutes=int(result.group(3)[:-1]))
            if result.group(4):
                parsed_time = parsed_time + timedelta(seconds=int(result.group(4)[:-1]))

    return parsed_time
