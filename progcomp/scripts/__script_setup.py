import os
import sys

parent = os.path.abspath(".")
sys.path.insert(1, parent)

import flask_migrate
from flask_migrate import Migrate

from progcomp import app
from progcomp.database import db
from progcomp.models import *

with app.app_context():
    migrate: Migrate = Migrate(app, db, render_as_batch=True)

script_progcomp = os.environ["SCRIPT_PROGCOMP"]
print("Current editing Progcomp:", script_progcomp)
