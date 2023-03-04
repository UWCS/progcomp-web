import enum
from datetime import datetime, timedelta
from typing import Optional, no_type_check


@no_type_check
def auto_str(cls: type[object]) -> type[object]:
    def __repr__(self):
        value = ", ".join(
            "{}={}".format(*item)
            for item in vars(self).items()
            if item[0] != "_sa_instance_state"
        )
        return f"{type(self).__name__} {{{value}}}"

    cls.__repr__ = __repr__
    return cls


DT = Optional[datetime]


def format_date(date: DT) -> str:
    if date is None:
        return ""
    return date.strftime("%a %d %b")


def format_time(time: DT) -> str:
    if time is None:
        return ""
    return time.strftime("%H:%M")


def format_datetime(dt: datetime) -> str:
    return format_date(dt) + " " + format_time(dt)


def date_str(dt: datetime, now: datetime) -> tuple[str, str]:
    if dt is None:
        return "", ""
    diff = max(now, dt) - min(now, dt)
    tense = "s" if now < dt else "ed"
    if diff.days > 9:
        return tense, format_date(dt)
    elif diff.days > 1:
        return tense, format_datetime(dt)
    else:
        return tense, format_time(dt)


def format_time_range(start: DT, end: DT, now: datetime):
    now = datetime.now()
    sten, start_str = date_str(start, now)
    enten, end_str = date_str(end, now)
    print(start_str, end_str)
    if start is None and end is None:
        return ""
    elif start is None or (end is not None and start < now):
        return f"End{enten}: {end_str}"
    else:
        return f"Start{sten}: {start_str}"


class Status(enum.Enum):
    UNKNOWN = 0
    SCORED = 1
    CORRECT = 2
    PARTIAL = 3
    WRONG = 4
    INVALID = 5


class Visibility(enum.Enum):
    HIDDEN = 0
    CLOSED = 1  # Visible but no submissions
    OPEN = 2

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __bool__(self):
        return self > Visibility.HIDDEN
