from collections import Counter
import logging
import os
from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, ForeignKeyConstraint, func
from sqlalchemy.orm import relationship

from progcomp.models.problem import Problem
from progcomp.models.submission import Submission
from progcomp.models.team import Team
from progcomp.models.utils import Status, auto_str

from ..database import db


@auto_str
class Progcomp(db.Model):
    __tablename__ = "progcomps"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    start_time = db.Column(db.DateTime, default=func.current_timestamp())
    show_leaderboard = db.Column(db.Boolean, nullable=False, default=False)

    teams = relationship(Team, back_populates="progcomp")
    problems = relationship(Problem, back_populates="progcomp", order_by=Problem.name)

    def get_team(self, name: str) -> Optional[Team]:
        return db.session.query(Team).filter(Team.name == name).first()

    def add_team(self, name: str, password: str):
        db.session.add(Team(progcomp_id=self.id, name=name, password=password))
        db.session.commit()

    def update_problems(self):
        # Add any new problems, update existing ones
        path = os.path.join(os.getcwd(), "problems")
        p_names = sorted(os.listdir(path))
        for p_name in p_names:
            prob = self.get_problem(p_name, False)
            if not prob:
                db.session.add(prob := Problem(name=p_name, progcomp_id=self.id, enabled=False))
            prob.update()
        db.session.commit()
        print("Problems", repr(self.problems))

    def get_problem(self, name, enabled_filter=True):
        q = db.session.query(Problem).where(Problem.name == name)
        if enabled_filter: q.where(Problem.enabled == True)
        return q.first()

    @property
    def enabled_problems(self):
        return (
            db.session.query(Problem)
            .where(Problem.enabled == True)
            .order_by(Problem.name)
            .all()
        )

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

    def score_teams(self):
        total = Counter()
        per_prob = []
        for problem in self.problems:
            if problem.tests[0].max_score:  # Has a max
                score = self.score_max(problem)
            else:   # Is optimisation
                score = self.score_optimisation(problem)
            per_prob.append(score)
            for t, s in score.items():
                total[t] += s
        
        actual = {}
        for team in self.teams:
            actual[team] = total[team.name]
        return actual

    def score_max(self, problem):
        score = Counter()
        print(problem)
        total = len(problem.tests)
        for test in problem.tests:
            test_scores = test.ranked_submissions
            print("\tTest Score", test.name, [(t.name, t.score) for t in test_scores])
            for sub in test_scores:
                if sub.status == Status.CORRECT:
                    score[sub.team.name] += 1. / total
                if sub.status == Status.PARTIAL:
                    score[sub.team.name] += (1. / 1.25) * sub.score / test.max_score / total
        print("Score", problem.name, score)
        return score
    
    def score_optimisation(self, problem):
        score = Counter()
        total = len(problem.tests)
        for test in problem.tests:
            test_scores = test.ranked_submissions
            print("\tTest Rank", test.name, [(t.name, t.score) for t in test_scores])
            for i, sub in enumerate(test_scores):
                score[sub.team.name] += (0.85 ** i) / total
        print("Score", problem.name, score)
        return score
