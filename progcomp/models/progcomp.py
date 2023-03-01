import os
from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import func, relationship

from progcomp.models.problem import Problem
from progcomp.models.submission import Submission
from progcomp.models.team import Team
from progcomp.models.utils import auto_str

from .. import db


@auto_str
class Progcomp(db.Model):
    __tablename__ = "progcomps"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    start_time = db.Column(db.DateTime, default=func.current_timestamp())

    teams = relationship("teams", back_populates="progcomp")
    problems = relationship("problems", back_populates="progcomp")

    def get_team(self, name: str) -> Optional[Team]:
        return db.query(Team).where(Team.name == name).first()

    def add_team(self, name: str, password: str):
        db.add(Team(progcomp_id=self.id, name=name, password=password))
        db.commit()

    def update_problems(self):
        # Add any new problems, update existing ones
        path = os.path.join(os.getcwd(), "problems")
        p_names = os.listdir(path)
        for p_name in p_names:
            prob = self.problems.get(p_name)
            if not prob:
                db.add(Problem(name=p_name, progcomp_id=self.id))
            else:
                prob.update()

    def get_problem(self, name):
        return db.query(Problem).where(Problem.name == name).first()

    def get_timestamp(self):
        td = datetime.now() - self.start_time
        return str(td)[:-4].replace(":", "-")

    def make_submission(
        self, timestamp: str, team_name: str, p_name: str, test_name: str
    ):
        team = self.get_team(team_name)
        problem = self.get_problem(p_name)
        if not team or not problem:
            return False
        test = problem.get_test(test_name)
        if not test:
            return False
        team.add_submission(
            Submission(team=team, problem=problem, test=test, timestamp=timestamp)
        )
        return True
