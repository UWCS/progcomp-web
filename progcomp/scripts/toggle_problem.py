from import_app import *

with app.app_context():
    pr = db.session.query(Problem).filter(Problem.name == sys.argv[1]).first()
    print(pr)
    pr.enabled = not pr.enabled
    print(pr)
    db.session.commit()
