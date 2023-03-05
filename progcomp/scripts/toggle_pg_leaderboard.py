from __script_setup import *

with app.app_context():
    pc = db.session.query(Progcomp).where(Progcomp.name == script_progcomp()).first()
    print(pc)
    pc.show_leaderboard = not pc.show_leaderboard
    print(pc)
    db.session.commit()
