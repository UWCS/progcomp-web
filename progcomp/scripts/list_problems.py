from import_app import *

with app.app_context():
    for problem in db.session.query(Problem).all():
        print("\n", problem)
        for test in problem.tests:
            print("\t", test)
