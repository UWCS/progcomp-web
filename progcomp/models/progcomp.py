import logging
import os
from collections import Counter, defaultdict
from datetime import datetime
from typing import Callable, Optional, Union

import sqlalchemy as sa
from sqlalchemy import ForeignKey, ForeignKeyConstraint, func
from sqlalchemy.orm import relationship

from progcomp.models import utils
from progcomp.models.alert import Alert
from progcomp.models.problem import Problem
from progcomp.models.submission import Submission
from progcomp.models.team import Team
from progcomp.models.utils import Status, Visibility, auto_str

from ..database import Base, db


@auto_str
class Progcomp(Base):
    __tablename__ = "progcomps"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    start_time = sa.Column(sa.DateTime, default=(dtnow := datetime.now().replace(second=0, microsecond=0)))
    show_leaderboard = sa.Column(
        sa.Boolean, nullable=False, default=False, server_default="f"
    )
    visibility = sa.Column(
        sa.Enum(Visibility),
        nullable=False,
        default=Visibility.OPEN,
        server_default="OPEN",
    )
    end_time = sa.Column(sa.DateTime)

    __table_args__ = (sa.UniqueConstraint("name", name="unq_progcomps_name"),)

    teams = relationship(Team, back_populates="progcomp")
    problems = relationship(Problem, back_populates="progcomp", order_by=Problem.name)
    alerts_r = relationship(Alert, back_populates="progcomp", order_by=Alert.start_time)

    @property
    def alerts(self) -> list[Alert]:
        return [a for a in self.alerts_r if a.visible]

    def alert_timestamps(self) -> list[datetime]:
        return [a.start_time.timestamp() for a in self.alerts]

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
    
    @property
    def all_problems(self) -> list[Problem]:
        problems = (
            db.session.query(Problem)
            .where(Problem.progcomp == self)
            .order_by(Problem.name)
            .all()
        )
        return [p for p in problems]
    
    @property
    def all_teams(self) -> list[Team]:
        teams = (
            db.session.query(Team)
            .where(Team.progcomp == self)
            .order_by(Team.name)
            .all()
        )
        return [t for t in teams]

    def update_problems(self) -> None:
        # Add any new problems, update existing ones
        path = os.path.join(os.getcwd(), "problems", self.name)
        p_names = sorted(os.listdir(path))
        print(f"\x1b[35m{p_names=}\x1b[0m")
        for p_name in p_names:
            if not os.path.isdir(os.path.join(path, p_name)):
                continue
            prob = self.get_problem(p_name, Visibility.HIDDEN)
            if not prob:
                prob = Problem(name=p_name, progcomp=self, visibility=Visibility.HIDDEN)
                db.session.add(prob)
                db.session.commit()
            prob.update()
        db.session.commit()
        print("Problems", repr(self.problems))

    def refresh_problems(self) -> None:
        # Remove all problems, then update them again
        problems = db.session.query(Problem).all()
        for prob in problems:
            db.session.delete(prob)
        db.session.commit()
        print("Problems", repr(self.problems))
        self.update_problems()

    def make_submission(
        self,
        directory: str,
        team_name: str,
        p_name: str,
        test_name: str,
        test_ext: str,
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

        conv: Callable[[Union[int, float]], int] = lambda x: round(x * 1000) / 10
        
        timestamps = self.timestamps()
        for problem in self.visible_problems:
            if problem.name == "0":
                continue
            if problem.tests[0].max_score:  # Has a max
                score = self.score_max(problem)
            else:  # Is optimisation
                score = self.score_optimisation(problem)
            timestamps = self.timestamps()
            per_prob.append(score)
            for t, s in score.items():
                total[t] += s

        actual: list[OverallScore] = []
        for team in self.teams:
            if team.blacklist:
                sk = -1
                sc = OverallScore(
                    team,
                    sk * len(per_prob),
                    [sk for _ in per_prob],
                    datetime.fromtimestamp(0)
                )
            else:
                sc = OverallScore(
                    team,
                    conv(total[team.name]),
                    [conv(per_prob[i][team.name]) for i in range(len(per_prob))],
                    timestamps.get(team.name, datetime.fromtimestamp(0))
                )
            actual.append(sc)
        
        # TODO: Fix (????)
        actual.sort(key=lambda x: (-x.total, x.timestamp))
        return actual

    def timestamps(self) -> dict[str, datetime]:
        """
        Returns a dictionary, which maps team names to their most recent submission to any test.
        """
        timestamps: dict[str, datetime] = {}
        for problem in self.problems:
            for test in problem.tests:
                for sub in test.ranked_submissions:
                    if sub.score == 0:
                        continue
                    cur_time = timestamps.get(sub.team.name, datetime.fromtimestamp(0))
                    timestamps[sub.team.name] = max(cur_time, sub.timestamp)
        return timestamps

    def score_max(self, problem: Problem) -> dict[str, float]:
        score: dict[str, float] = defaultdict(float)
        total = len(problem.tests)
        for test in problem.tests:
            weight = test.weight if test.weight else 1

            test_scores = test.ranked_submissions
            print(
                "\tTest Score", weight, test.name, [(t.team.name, t.score) for t in test_scores]
            )
            for sub in test_scores:
                print(f"\x1b[35mtest: {test} | sub: {sub}\x1b[0m")
                if sub.status == Status.CORRECT:
                    score[sub.team.name] += weight * 1.25 / total # TODO: HUHHH?????
                if sub.status == Status.PARTIAL:
                    score[sub.team.name] += weight * float(sub.score) / test.max_score / total
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
    def __init__(self, team, total, per_round, timestamp) -> None:
        self.team = team
        self.total = total
        self.per_round = per_round
        self.timestamp = timestamp

    @property
    def time_str(self) -> str:
        return self.timestamp.strftime("%c")
