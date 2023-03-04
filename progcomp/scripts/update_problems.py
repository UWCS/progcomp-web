from __script_setup import *

with app.app_context():
    pc = db.session.query(Progcomp).where(Progcomp.name == "main").first()
    print(pc)
    pc.update_problems()
