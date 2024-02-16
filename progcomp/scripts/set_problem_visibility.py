from __script_setup import *

level = sys.argv[2].lower()
if level == "open":
    level = Visibility.OPEN
elif level == "closed":
    level = Visibility.CLOSED
elif level == "hidden":
    level = Visibility.HIDDEN
else:
    raise ValueError("Level must be one of `open`, `closed` or `hidden`.")

with app.app_context():
    pc = db.session.query(Progcomp).where(Progcomp.name == script_progcomp()).first()
    pr = (
        db.session.query(Problem)
        .filter(Problem.progcomp_id == pc.id)
        .filter(Problem.name == sys.argv[1])
        .first()
    )
    print(pr)
    pr.visibility = level
    print(pr)
    db.session.commit()
