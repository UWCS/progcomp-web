import os
import sys

import flask_migrate

parent = os.path.abspath(".")
sys.path.insert(1, parent)

from progcomp import app
from progcomp.database import db
from progcomp.models import *

script_progcomp = os.environ["SCRIPT_PROGCOMP"]
print("Current editing Progcomp:", script_progcomp)
