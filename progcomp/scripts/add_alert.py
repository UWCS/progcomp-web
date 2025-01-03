import __utils
from __script_setup import *

with app.app_context():
    if len(sys.argv) == 1:
        print(
            f"\x1b[36mUsage: python {sys.argv[0]} <name> <start_time> <end_time> <title> <text>\x1b[0m"
        )
        exit(0)

    start_time = __utils.parse_time(sys.argv[2])
    end_time = __utils.parse_time(sys.argv[3])
    title = sys.argv[4]
    if len(sys.argv) == 6:
        title, text = sys.argv[4], sys.argv[5]
    else:
        title, text = None, sys.argv[4]

    pc = db.session.query(Progcomp).where(Progcomp.name == script_progcomp()).first()
    db.session.add(
        alert := Alert(
            name=sys.argv[1],
            progcomp=pc,
            start_time=start_time,
            end_time=end_time,
            title=title,
            text=text,
        )
    )
    print(alert)
    db.session.commit()
