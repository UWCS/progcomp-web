from __script_setup import *

with app.app_context():
    db.session.add(pc := Progcomp(name=sys.argv[1], visibility=Visibility.HIDDEN))
    print(pc)
    db.session.commit()

    print(">>> REMEMBER TO UPDATE ENV VAR: `SCRIPT_PROGCOMP` <<<")
