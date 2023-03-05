import logging
import os
from collections import Counter, defaultdict
from datetime import datetime
from typing import Callable, Optional, Union

import sqlalchemy as sa
from sqlalchemy import ForeignKey, ForeignKeyConstraint, func
from sqlalchemy.orm import relationship

from progcomp.models import utils
from progcomp.models.problem import Problem
from progcomp.models.submission import Submission
from progcomp.models.team import Team
from progcomp.models.utils import Status, Visibility, auto_str

from ..database import Base, db


@auto_str
class Alert(Base):
    __tablename__ = "alerts"

    id = sa.Column(sa.Integer, primary_key=True)
    progcomp_id = sa.Column(sa.Integer, ForeignKey("progcomps.id"))
    name = sa.Column(sa.String)
    start_time = sa.Column(sa.DateTime, default=func.current_timestamp())
    end_time = sa.Column(sa.DateTime)

    progcomp = relationship("Progcomp", back_populates="alerts_r")

    @property
    def visible(self) -> bool:
        now = datetime.now()
        return self.start_time < now and (not self.end_time or now < self.end_time)
