import logging
import os

from flask import Flask

from .database import db, migrate

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.getLevelName("INFO"),
    format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("progcomp.log"),
        logging.StreamHandler(),
    ],
)


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ["SECRET_KEY"],
        MAX_CONTENT_LENGTH=1000 * 1000 * 1000,  # 1gb,
        SQLALCHEMY_DATABASE_URI=os.environ["DATABASE_URL"],
    )

    db.init_app(app)
    migrate.init_app(app, db)

    from . import routes

    app.register_blueprint(routes.bp)
    return app


app: Flask = create_app()
