import typing

import flask_migrate
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()

migrate: Migrate = Migrate()

if typing.TYPE_CHECKING:
    from flask_sqlalchemy.model import Model

    Base = db.make_declarative_base(Model)
else:
    Base = db.Model
