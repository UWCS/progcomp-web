from __script_setup import *

with app.app_context():
    pc = db.session.query(Progcomp).where(Progcomp.name == script_progcomp()).first()

    confirm = input(f"\x1b[31mYou are about to delete the following Progcomp:\n\n{pc}\n\nAre you sure? \x1b[0m")
    if confirm.lower()[0] == "y":
        db.session.delete(pc)
        db.session.commit()

        remaining = list(db.session.query(Progcomp))
        print(f"\x1b[32mRemaining: {remaining}\x1b[0m")
