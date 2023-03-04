from __script_setup import *

with app.app_context():
    for pc in db.session.query(Progcomp).all():
        print("\n", pc)
        for problem in pc.problems:
            print("\n\t", problem)
            for test in problem.tests:
                print("\t\t", test)
