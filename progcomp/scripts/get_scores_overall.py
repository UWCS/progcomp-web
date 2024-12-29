from __script_setup import *

with app.app_context():
    pc = db.session.query(Progcomp).where(Progcomp.name == script_progcomp()).first()
    scores = pc.score_teams()
    print("========================= Overall Leaderboard =========================")
    for s in scores:
        print(s.team.name, s.total, s.per_round)
