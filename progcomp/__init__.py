import logging
import os

from flask import Flask

from progcomp.models.progcomp import Progcomp

logging.basicConfig(
    level=logging.getLevelName("INFO"),
    format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("progcomp.log"),
        logging.StreamHandler(),
    ],
)

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY="dev",
    MAX_CONTENT_LENGTH=20 * 1000 * 1000,  # 20mb,
    SQLALCHEMY_DATABASE_URI=os.environ["DATABASE_URL"],
)

from .database import db

db.init_app(app)

from flask_alembic import Alembic

alembic = Alembic()
alembic.init_app(app)

# COMMENT OUT FOLLOWING WHEN ALEMBIC-ING
print("NAME", __name__)
from . import routes

app.register_blueprint(routes.bp)
