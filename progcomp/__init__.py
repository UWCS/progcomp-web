import logging
import os

from flask import Flask

from .database import db

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
        SECRET_KEY="dev",
        MAX_CONTENT_LENGTH=30 * 1000 * 1000,  # 20mb,
        SQLALCHEMY_DATABASE_URI=os.environ["DATABASE_URL"],
    )

    db.init_app(app)

    from . import routes

    app.register_blueprint(routes.bp)
    return app


app: Flask = create_app()
