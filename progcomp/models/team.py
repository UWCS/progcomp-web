from sqlalchemy import ForeignKey, ForeignKeyConstraint, func
from sqlalchemy.orm import relationship

from progcomp.models.utils import auto_str

from ..database import db


@auto_str
class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    progcomp_id = db.Column(db.Integer, ForeignKey("progcomps.id"))
    name = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)
    score = db.Column(db.Integer, default=0)

    submissions = relationship("Submission", back_populates="team")
    # , order_by="submissions.timestamp"
    progcomp = relationship("Progcomp", back_populates="teams")
