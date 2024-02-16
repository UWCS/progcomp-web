import __utils
from __script_setup import *

with app.app_context():
    name = sys.argv[1]
    pc = db.session.query(Progcomp).where(Progcomp.name == script_progcomp()).first()
    print(pc.alerts_r)
    alert = next(a for a in pc.alerts_r if a.name == name)
    print(alert)
    db.session.delete(alert)
    db.session.commit()
