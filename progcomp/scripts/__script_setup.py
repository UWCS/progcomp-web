import os
import sys

import flask_migrate

parent = os.path.abspath(".")
sys.path.insert(1, parent)

from progcomp import app
from progcomp.database import db
from progcomp.models import *

_script_progcomp: str = None


def script_progcomp():
    global _script_progcomp
    if _script_progcomp is None:
        _script_progcomp = os.environ["SCRIPT_PROGCOMP"]
        print("Current editing Progcomp:", _script_progcomp)
    return _script_progcomp
