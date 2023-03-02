from __script_setup import *

prob = sys.argv[1]
test = sys.argv[2]
with app.app_context():
    pr = db.session.query(Problem).filter(Problem.name == prob).first()
    print(pr)
    test = pr.get_test(test)
    # print(test.ranked_submissions)
    for sub in test.ranked_submissions:
        logging.info(
            f"Submission {sub.problem.name}: {sub.test.name} by {sub.team.name} [{sub.status}] {sub.score}/{sub.test.max_score or ''}"
        )
