import os
import sys

parent = os.path.abspath(".")
sys.path.insert(1, parent)

from progcomp import app
from progcomp.database import alembic, db
