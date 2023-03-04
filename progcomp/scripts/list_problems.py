from __script_setup import *

with app.app_context():
    print(db.session.query(Progcomp).first())
    for problem in db.session.query(Problem).all():
        print("\n", problem)
        for test in problem.tests:
            print("\t", test)
