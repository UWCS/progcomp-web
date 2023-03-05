import __utils
from __script_setup import *

with app.app_context():
    start_time = __utils.parse_time(sys.argv[2])
    end_time = __utils.parse_time(sys.argv[3])
    pc = db.session.query(Progcomp).where(Progcomp.name == script_progcomp()).first()
    db.session.add(
        alert := Alert(
            name=sys.argv[1],
            start_time=start_time,
            end_time=end_time,
            title=sys.argv[4],
            text=sys.argv[5],
        )
    )
    print(alert)
    db.session.commit()
