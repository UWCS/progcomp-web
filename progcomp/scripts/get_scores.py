from import_app import *

prob = sys.argv[1]
test = sys.argv[2]
with app.app_context():
    pr = db.session.query(Problem).filter(Problem.name == prob).first()
    print(pr)
    test = pr.get_test(test)
    print(test.ranked_submissions)
