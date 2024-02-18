from __script_setup import *

with app.app_context():
    pc = db.session.query(Progcomp).where(Progcomp.name == script_progcomp()).first()
    for team in db.session.query(Team).where(Team.progcomp_id == pc.id).all():
        print(">>>", team.submissions)
