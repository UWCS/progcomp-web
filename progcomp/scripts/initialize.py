from import_app import *

with app.app_context():
    alembic.upgrade()
