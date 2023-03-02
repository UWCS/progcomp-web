from __script_setup import *

if len(sys.argv) < 2:
    print("Provide a revision name")
    sys.exit()

with app.app_context():
    alembic.revision(sys.argv[1])
    input("Press enter to upgrade to revision\n>>>")
    alembic.upgrade()
