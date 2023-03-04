import __utils
from __script_setup import *

with app.app_context():
    new_time = __utils.parse_time(sys.argv[1])
    pc = db.session.query(Progcomp).where(Progcomp.name == script_progcomp).first()
    print("Old", pc.start_time)
    print("New", new_time)
    pc.start_time = new_time
    db.session.commit()
