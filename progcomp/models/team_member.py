import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from progcomp.models.utils import auto_str

from ..database import Base, db


@auto_str
class TeamMember(Base):
    __tablename__ = "team_members"

    id = sa.Column(sa.String, primary_key=True)
    team_id = sa.Column(sa.Integer, ForeignKey("teams.id"))

    __table_args__ = (sa.UniqueConstraint("id", "team_id"),)

    team = relationship("Team", back_populates="members")
