from __script_setup import *

with app.app_context():
    flask_migrate.upgrade()
