from __script_setup import *

with app.app_context():
    pc = db.session.query(Progcomp).first()
    problem = pc.visible_problems[0]
    test = problem.tests[0]
    test_scores = test.ranked_submissions
    print("Problem:", problem)
    for sc in test_scores:
        print("~" * 80)
        print(sc)
        print()
        print("~" * 80)
