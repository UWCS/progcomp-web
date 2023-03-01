from import_app import *

with app.app_context():
    pc = db.session.query(Progcomp).first()
    print(pc.score_teams())
    for s in pc.score_teams():
        print(s.team.name, s.total, s.per_round)
