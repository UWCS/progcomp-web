import sqlalchemy as sa
from sqlalchemy import ForeignKey, ForeignKeyConstraint, desc
from sqlalchemy.orm import relationship

from progcomp.models.team_member import TeamMember
from progcomp.models.submission import Submission
from progcomp.models.utils import auto_str

from ..database import Base, db


@auto_str
class Team(Base):
    __tablename__ = "teams"

    id = sa.Column(sa.Integer, primary_key=True)
    progcomp_id = sa.Column(sa.Integer, ForeignKey("progcomps.id"))
    name = sa.Column(sa.String)
    password = sa.Column(sa.String, nullable=False)
    score = sa.Column(sa.Integer, default=0)
    blacklist = sa.Column(sa.Boolean, default=False)

    __table_args__ = (sa.UniqueConstraint("name", "progcomp_id", name="unq_team_name"),)

    submissions = relationship(
        "Submission", back_populates="team", order_by=Submission.timestamp.desc()
    )
    # , order_by="submissions.timestamp"
    progcomp = relationship("Progcomp", back_populates="teams")
    members = relationship("TeamMember", back_populates="team")

    @property
    def member_ids(self) -> list[str]:
        return [member.id for member in self.members]

    def add_member(self, member_id):
        db.session.add(TeamMember(id=member_id, team_id=self.id))
        db.session.commit()
