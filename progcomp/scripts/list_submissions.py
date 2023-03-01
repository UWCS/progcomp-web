from import_app import *

with app.app_context():
    for team in db.session.query(Team).all():
        print("\n", team)
        for sub in team.submissions:
            print("\t", sub)
