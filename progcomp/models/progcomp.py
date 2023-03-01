import logging
import os
from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, ForeignKeyConstraint, func
from sqlalchemy.orm import relationship

from progcomp.models.problem import Problem
from progcomp.models.submission import Submission
from progcomp.models.team import Team
from progcomp.models.utils import auto_str

from ..database import db


@auto_str
class Progcomp(db.Model):
    __tablename__ = "progcomps"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    start_time = db.Column(db.DateTime, default=func.current_timestamp())

    teams = relationship(Team, back_populates="progcomp")
    problems = relationship(Problem, back_populates="progcomp")

    def get_team(self, name: str) -> Optional[Team]:
        return db.session.query(Team).filter(Team.name == name).first()

    def add_team(self, name: str, password: str):
        db.session.add(Team(progcomp_id=self.id, name=name, password=password))
        db.session.commit()

    def update_problems(self):
        # Add any new problems, update existing ones
        path = os.path.join(os.getcwd(), "problems")
        p_names = os.listdir(path)
        for p_name in p_names:
            prob = self.get_problem(p_name)
            if not prob:
                db.session.add(prob := Problem(name=p_name, progcomp_id=self.id))
            prob.update()
        db.session.commit()
        print("Problems", repr(self.problems))

    def get_problem(self, name):
        return db.session.query(Problem).where(Problem.name == name).first()

    def get_timestamp_str(self, time):
        return time.strftime("%Y-%m-%d_%H-%M-%S")

    def make_submission(
        self,
        directory: str,
        team_name: str,
        p_name: str,
        test_name: str,
        timestamp: datetime,
    ):
        team = self.get_team(team_name)
        problem = self.get_problem(p_name)
        if not team or not problem:
            return False
        test = problem.get_test(test_name)
        if not test:
            return False
        db.session.add(
            sub := Submission(
                team=team,
                problem=problem,
                test=test,
                timestamp=timestamp,
                directory=directory,
            )
        )
        print("New sub", sub)
        sub.mark()
        db.session.commit()
        return True
