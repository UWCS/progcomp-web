import enum


def auto_str(cls):
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
