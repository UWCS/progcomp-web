import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = None


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config.from_mapping(
        SECRET_KEY="dev",
        MAX_CONTENT_LENGTH=20 * 1000 * 1000,  # 20mb,
        SQLALCHEMY_DATABASE_URI=os.environ["DATABASE_URL"],
    )

    global db
    db = SQLAlchemy(app)

    from . import routes

    app.register_blueprint(routes.bp)

    return app


app = create_app()
