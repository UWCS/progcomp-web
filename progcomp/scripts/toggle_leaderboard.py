from import_app import *

with app.app_context():
    pc = db.session.query(Progcomp).first()
    print(pc)
    pc.show_leaderboard = not pc.show_leaderboard
    print(pc)
    db.session.commit()
