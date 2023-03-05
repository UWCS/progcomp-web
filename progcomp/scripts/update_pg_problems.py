from __script_setup import *

with app.app_context():
    pc = db.session.query(Progcomp).where(Progcomp.name == script_progcomp()).first()
    print(pc)
    pc.update_problems()
