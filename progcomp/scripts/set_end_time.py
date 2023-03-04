import __utils
from __script_setup import *

with app.app_context():
    new_time = __utils.parse_time(sys.argv[1])
    pc = db.session.query(Progcomp).where(Progcomp.name == "main").first()
    print("Old", pc.end_time)
    print("New", new_time)
    pc.end_time = new_time
    db.session.commit()
