import enum
import typing


@typing.no_type_check
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
