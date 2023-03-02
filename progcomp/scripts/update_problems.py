from __script_setup import *

with app.app_context():
    pc = db.session.query(Progcomp).first()
    print(pc)
    pc.update_problems()
