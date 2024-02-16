from __script_setup import *

with app.app_context():
    pc = db.session.query(Progcomp).first()
    problem = pc.get_problem("0")
    print(problem)
    print(problem.tests)
