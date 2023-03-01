from import_app import *

with app.app_context():
    pc = db.session.query(Progcomp).first()
    print(pc.score_teams())