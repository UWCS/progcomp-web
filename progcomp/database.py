import typing

from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()


if typing.TYPE_CHECKING:
    from flask_sqlalchemy.model import Model

    Base = db.make_declarative_base(Model)
else:
    Base = db.Model
