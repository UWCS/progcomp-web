import os
import sys

parent = os.path.abspath(".")
sys.path.insert(1, parent)

from flask_alembic import Alembic

from progcomp import app
from progcomp.database import db
from progcomp.models import *

with app.app_context():
    alembic: Alembic = Alembic()
    alembic.init_app(app)
