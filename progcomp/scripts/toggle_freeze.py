from import_app import *

with app.app_context():
    pc = db.session.query(Progcomp).first()
    print(pc)
    pc.freeze = not pc.freeze
    print(pc)
    db.session.commit()
