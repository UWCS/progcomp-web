import logging
import os
from collections import Counter, defaultdict
from datetime import datetime
from typing import Callable, Optional, Union

from sqlalchemy import ForeignKey, ForeignKeyConstraint, func
from sqlalchemy.orm import relationship

from progcomp.models import utils
from progcomp.models.problem import Problem
from progcomp.models.submission import Submission
from progcomp.models.team import Team
from progcomp.models.utils import Status, Visibility, auto_str

from ..database import Base, db


@auto_str
class Progcomp(Base):
    __tablename__ = "progcomps"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    start_time = db.Column(db.DateTime, default=func.current_timestamp())
    show_leaderboard = db.Column(
        db.Boolean, nullable=False, default=False, server_default="f"
    )
    visibility = db.Column(
        db.Enum(Visibility),
        nullable=False,
        default=Visibility.OPEN,
        server_default="OPEN",
    )
    end_time = db.Column(db.DateTime)

    teams = relationship(Team, back_populates="progcomp")
    problems = relationship(Problem, back_populates="progcomp", order_by=Problem.name)

    @property
    def visible(self) -> Visibility:
        return self.visibility

    @property
    def open(self) -> bool:
        return self.visible == Visibility.OPEN

    def get_timestamp_str(self, time) -> str:
        return utils.time_str(time, datetime.now())

    @property
    def time_str(self) -> str:
        return utils.format_time_range(self.start_time, self.end_time, datetime.now())

    @property
    def category(self) -> str:
        now = datetime.now()
        if self.start_time and now < self.start_time:
            return "Upcoming"
        elif self.end_time and self.end_time < now:
            return "Archived"
        elif self.start_time and self.end_time:
            # If both exist, must be betweeen
            return "Active"
        else:
            return "Unknown"

    def get_team(self, name: str) -> Optional[Team]:
        return (
            db.session.query(Team)
            .where(Team.progcomp == self)
            .filter(Team.name == name)
            .first()
        )

    def add_team(self, name: str, password: str) -> None:
        db.session.add(Team(progcomp_id=self.id, name=name, password=password))
        db.session.commit()

    def get_problem(self, name, visibility=Visibility.CLOSED) -> Optional[Problem]:
        problems = (
            db.session.query(Problem)
            .where(Problem.progcomp == self)
            .where(Problem.name == name)
            .all()
        )
        return next((p for p in problems if p.visible >= visibility), None)

    @property
    def visible_problems(self) -> list[Problem]:
        problems = (
            db.session.query(Problem)
            .where(Problem.progcomp == self)
            .order_by(Problem.name)
            .all()
        )
        return [p for p in problems if p.visible]

    def update_problems(self) -> None:
        # Add any new problems, update existing ones
        path = os.path.join(os.getcwd(), "problems", self.name)
        p_names = sorted(os.listdir(path))
        for p_name in p_names:
            if not os.path.isdir(os.path.join(path, p_name)):
                continue
            prob = self.get_problem(p_name, Visibility.HIDDEN)
            if not prob:
                prob = Problem(name=p_name, progcomp=self, visibility=Visibility.HIDDEN)
                db.session.add(prob)
            prob.update()
        db.session.commit()
        print("Problems", repr(self.problems))

    def make_submission(
        self,
        directory: str,
        team_name: str,
        p_name: str,
        test_name: str,
        timestamp: datetime,
    ) -> bool:
        team = self.get_team(team_name)
        problem = self.get_problem(p_name)
        if not team or not problem:
            return False
        if not (test := problem.get_test(test_name)):
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
        sub.mark()
        print("New sub", sub)
        db.session.commit()
        return True

    def score_teams(self) -> list["OverallScore"]:
        total: dict[str, float] = defaultdict(float)
        per_prob = []

        conv: Callable[[Union[int, float]], int] = lambda x: round(x * 100)
        for problem in self.visible_problems:
            if problem.name == "0":
                continue
            if problem.tests[0].max_score:  # Has a max
                score = self.score_max(problem)
            else:  # Is optimisation
                score = self.score_optimisation(problem)
            per_prob.append(score)
            for t, s in score.items():
                total[t] += s

        actual: list[OverallScore] = []
        for team in self.teams:
            sc = OverallScore(
                team,
                conv(total[team.name]),
                [conv(per_prob[i][team.name]) for i in range(len(per_prob))],
            )
            actual.append(sc)
        actual.sort(key=lambda x: x.total)
        actual.reverse()
        return actual

    def score_max(self, problem: Problem) -> dict[str, float]:
        score: dict[str, float] = defaultdict(float)
        print(problem)
        total = len(problem.tests)
        for test in problem.tests:
            test_scores = test.ranked_submissions
            print(
                "\tTest Score", test.name, [(t.team.name, t.score) for t in test_scores]
            )
            for sub in test_scores:
                if sub.status == Status.CORRECT:
                    score[sub.team.name] += 1.25 / total
                if sub.status == Status.PARTIAL:
                    score[sub.team.name] += float(sub.score) / test.max_score / total
        print("Score", problem.name, score)
        return score

    def score_optimisation(self, problem) -> dict[str, float]:
        score: dict[str, float] = defaultdict(float)
        total = len(problem.tests)
        for test in problem.tests:
            test_scores = test.ranked_submissions
            print(
                "\tTest Rank", test.name, [(t.team.name, t.score) for t in test_scores]
            )
            for i, sub in enumerate(test_scores):
                if sub.score > 0:
                    score[sub.team.name] += 1.25 * (0.85**i) / total
        print("Score", problem.name, score)
        return score


@auto_str
class OverallScore:
    def __init__(self, team, total, per_round) -> None:
        self.team = team
        self.total = total
        self.per_round = per_round
